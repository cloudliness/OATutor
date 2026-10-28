import React, { createRef } from "react";
import Grid from "@material-ui/core/Grid";
import TextField from "@material-ui/core/TextField";
import MultipleChoice from "./MultipleChoice";
import GridInput from "./GridInput";
import MatrixInput from "./MatrixInput";
import { renderText } from "../../platform-logic/renderText";
import clsx from "clsx";
import "mathlive";
import './ProblemInput.css'
import { shuffleArray } from "../../util/shuffleArray";
import { EQUATION_EDITOR_AUTO_COMMANDS, EQUATION_EDITOR_AUTO_OPERATORS, ThemeContext } from "../../config/config";
import { stagingProp } from "../../util/addStagingProperty";
import { parseMatrixTex } from "../../util/parseMatrixTex";
import withWidth from "@material-ui/core/withWidth";
import { isMobileWidth } from "../../util/responsive";
import { showMathKeyboardAnimated, hideMathKeyboardAnimated, isMathKeyboardShowSuppressed } from "./mathKeyboardGestures";

function wantsNativeKeyboard() {
    if (typeof window === "undefined") return false;
    const coarse = window.matchMedia?.("(pointer: coarse)")?.matches;
    return Boolean(coarse) || window.innerWidth < 960;
}

class ProblemInput extends React.Component {
    static contextType = ThemeContext;

    constructor(props) {
        super(props);

        this.equationRef = createRef()

        this.mathFieldRef = React.createRef();

        this.onEquationChange = this.onEquationChange.bind(this)
        
        this.state = {
            value: "",
            isMathFieldFocused: false,
            mathKeypad: false,
        };
    }

    componentDidMount() {
        document.addEventListener('pointerdown', this.handleClickOutside, true);
        window.addEventListener('oat-math-kb', this.handleKeyboardVisibility);
        if (window.visualViewport) {
            window.visualViewport.addEventListener('resize', this.keepFieldVisible);
            window.visualViewport.addEventListener('scroll', this.keepFieldVisible);
        }
        this.attachMathField();
        this.applyKeyboardLayout();

        console.debug('problem', this.props.step, 'seed', this.props.seed)
        if (this.isMatrixInput()) {
            console.log('automatically determined matrix input to be the correct problem type')
        }

        const mqDisplayArea = this.equationRef?.current?.querySelector(".mq-editable-field > .mq-root-block")
        if (mqDisplayArea != null) {
            mqDisplayArea.ariaHidden = true
        }

        const textareaEl = this.equationRef?.current?.querySelector(".mq-textarea > textarea")
        if (textareaEl != null) {
            textareaEl.ariaLabel = `Answer question number ${this.props.index} here`
        }
    }

    componentDidUpdate(prevProps) {
        if (prevProps.keyboardType !== this.props.keyboardType) {
            this.applyKeyboardLayout();
        }
        const field = this.mathFieldRef.current;
        if (!field) return;
        const stepChanged = prevProps.step?.id !== this.props.step?.id
            || prevProps.index !== this.props.index;
        if (stepChanged) {
            const next = typeof this.props.state?.inputVal === 'string' ? this.props.state.inputVal : '';
            if (field.value !== next) field.value = next;
        }
    }

    componentWillUnmount() {
        document.removeEventListener('pointerdown', this.handleClickOutside, true);
        window.removeEventListener('oat-math-kb', this.handleKeyboardVisibility);
        if (window.visualViewport) {
            window.visualViewport.removeEventListener('resize', this.keepFieldVisible);
            window.visualViewport.removeEventListener('scroll', this.keepFieldVisible);
        }
        if (this._blurHideTimer) {
            clearTimeout(this._blurHideTimer);
            this._blurHideTimer = null;
        }
        if (this._mathField && this._onMathInput) {
            this._mathField.removeEventListener('input', this._onMathInput);
        }
    }

    attachMathField = () => {
        const field = this.mathFieldRef.current;
        if (!field || field.dataset.oatBound === '1') return;
        if (!field.shadowRoot?.querySelector('.ML__keyboard-sink')) return;
        field.dataset.oatBound = '1';
        this._mathField = field;
        this._onMathInput = () => this.publishMathValue(field);
        field.addEventListener('input', this._onMathInput);
        // Capture runs before MathLive's bubble pointerdown, which calls
        // preventDefault() and cancels the focus that would open Android's IME.
        field.addEventListener('pointerdown', this.handleMathFieldPointerDown, true);
        if (wantsNativeKeyboard()) {
            try {
                field.mathVirtualKeyboardPolicy = 'manual';
            } catch (_) {
                // attribute on the element still applies at connect time
            }
        }
        this.bridgeAndroidIme(field);
        const initial = this.props.state?.inputVal;
        if (typeof initial === 'string' && initial && field.value !== initial) {
            field.value = initial;
        }
    };

    publishMathValue = (field) => {
        const next = typeof field?.value === 'string' ? field.value : '';
        if (next !== this.props.state?.inputVal) {
            this.props.setInputValState(next);
        }
    };

    /**
     * MathLive's keyboard sink is clipped to an empty box with inputmode=none
     * so its own keypad can replace the OS keyboard. Android Chrome, and an
     * installed standalone app in particular, will not open the system keyboard
     * for that node. Give the sink a real box and a numeric input mode.
     */
    prepareNativeSink = (field) => {
        const sink = field?.shadowRoot?.querySelector('.ML__keyboard-sink');
        if (!sink || !wantsNativeKeyboard()) return sink || null;
        sink.setAttribute('enterkeyhint', 'done');
        sink.setAttribute('autocapitalize', 'off');
        sink.style.position = 'absolute';
        sink.style.inset = '0';
        sink.style.width = '100%';
        sink.style.height = '100%';
        sink.style.opacity = '1';
        sink.style.color = 'transparent';
        sink.style.background = 'transparent';
        sink.style.clip = 'auto';
        sink.style.clipPath = 'none';
        sink.style.fontSize = '16px';
        sink.style.lineHeight = '1';
        sink.style.pointerEvents = 'none';
        sink.style.caretColor = 'transparent';
        sink.style.overflow = 'hidden';
        return sink;
    };

    /**
     * Android Chrome / Gboard delivers text through beforeinput on the hidden
     * keyboard sink (often keyCode 229) and MathLive 0.109 sometimes drops it.
     * If the visible value did not change, insert the character ourselves.
     */
    bridgeAndroidIme = (field) => {
        const sink = this.prepareNativeSink(field) || field.shadowRoot?.querySelector('.ML__keyboard-sink');
        if (!sink || sink.dataset.oatIme === '1') return;
        sink.dataset.oatIme = '1';
        sink.setAttribute('enterkeyhint', 'done');
        sink.setAttribute('autocapitalize', 'off');

        const syncInputMode = () => {
            if (!wantsNativeKeyboard()) return;
            const virtualOpen = Boolean(window.mathVirtualKeyboard?.visible);
            // inputmode=none is what hides Android's keyboard. Use it only while
            // the in-app math keypad is actually open.
            const mode = virtualOpen ? 'none' : 'decimal';
            sink.setAttribute('inputmode', mode);
            field.setAttribute('inputmode', mode);
        };
        syncInputMode();
        this._syncImeMode = syncInputMode;

        const insertIfIgnored = (data) => {
            const text = typeof data === 'string' ? data.replace(/\u200b/g, '') : '';
            if (!text) return;
            const before = field.value || '';
            queueMicrotask(() => {
                if (!field.isConnected) return;
                if ((field.value || '') !== before) return;
                try {
                    field.executeCommand(['insert', text]);
                } catch (err) {
                    field.value = before + text;
                }
                sink.textContent = '';
                this.publishMathValue(field);
                this.keepFieldVisible();
            });
        };

        sink.addEventListener('beforeinput', (event) => {
            if (!event.inputType || !event.inputType.startsWith('insert')) return;
            insertIfIgnored(event.data);
        }, true);
        sink.addEventListener('input', (event) => {
            const data = event.data || sink.textContent || '';
            insertIfIgnored(data);
        }, true);
        sink.addEventListener('compositionend', (event) => {
            insertIfIgnored(event.data || sink.textContent || '');
        }, true);
    };

    keepFieldVisible = () => {
        const field = this.mathFieldRef.current;
        if (!field) return;
        // Scrolling in response to the native IME's visualViewport resize
        // blurs the field and dismisses Android's keyboard.
        if (wantsNativeKeyboard() && !window.mathVirtualKeyboard?.visible) return;
        const viewport = window.visualViewport;
        const visibleBottom = viewport
            ? viewport.offsetTop + viewport.height
            : window.innerHeight;
        const keyboard = document.querySelector('body > .ML__keyboard.is-visible .MLK__backdrop');
        const keyboardTop = keyboard ? keyboard.getBoundingClientRect().top : visibleBottom;
        const limit = Math.min(visibleBottom, keyboardTop) - 12;
        const rect = field.getBoundingClientRect();
        if (rect.bottom > limit - 8) {
            field.scrollIntoView({ block: 'center', inline: 'nearest' });
        }
    };

    handleKeyboardVisibility = (event) => {
        if (this._syncImeMode) this._syncImeMode();
        const open = Boolean(event?.detail?.open);
        if (this.state.mathKeypad !== open) this.setState({ mathKeypad: open });
        if (open) {
            window.setTimeout(this.keepFieldVisible, 60);
            window.setTimeout(this.keepFieldVisible, 320);
        }
    };

    /**
     * Setting layouts rebuilds the MathLive keyboard DOM. Never do that from
     * render() (accordion collapse re-renders mid-dismiss and causes slide-up).
     */
    applyKeyboardLayout = () => {
        if (typeof window === 'undefined') return;
        if (isMathKeyboardShowSuppressed()) return;
        const kb = window.mathVirtualKeyboard;
        if (!kb) return;
        const keyboardType = this.props.keyboardType;
        try {
            kb.layouts = keyboardType ? [keyboardType] : ["default"];
        } catch {
            try {
                kb.layouts = ["default"];
            } catch (_) {
                // ignore
            }
        }
    };

    /**
     * Android only shows the IME if a contenteditable is focused synchronously
     * inside the tap. Standalone PWAs also ignore inputmode=none, which is
     * MathLive's default on its hidden sink, so the native keyboard never opens
     * and the in-app keypad was being requested too late to replace it.
     */
    focusNativeKeyboard = () => {
        const field = this.mathFieldRef.current;
        const sink = this.prepareNativeSink(field);
        if (!field || !sink) return;
        field.setAttribute('inputmode', 'decimal');
        sink.setAttribute('inputmode', 'decimal');
        sink.setAttribute('enterkeyhint', 'done');
        try {
            sink.focus({ preventScroll: true });
        } catch (err) {
            try {
                field.focus({ preventScroll: true });
            } catch (_) {
                field.focus();
            }
        }
    };

    handleMathFieldPointerDown = (event) => {
        if (!wantsNativeKeyboard()) return;
        if (event.button != null && event.button !== 0) return;
        const path = typeof event.composedPath === 'function' ? event.composedPath() : [];
        const isBuiltInToggle = path.some((el) => {
            const part = el?.getAttribute?.('part');
            return (
                el?.classList?.contains?.('ML__virtual-keyboard-toggle') ||
                el?.classList?.contains?.('ML__menu-toggle') ||
                part === 'virtual-keyboard-toggle' ||
                part === 'menu-toggle'
            );
        });
        if (isBuiltInToggle) return;
        if (window.mathVirtualKeyboard?.visible) return;
        this.focusNativeKeyboard();
        const field = this.mathFieldRef.current;
        if (field && typeof field.getOffsetFromPoint === 'function') {
            try {
                const offset = field.getOffsetFromPoint(event.clientX, event.clientY, { bias: 0 });
                if (typeof offset === 'number' && offset >= 0) field.position = offset;
            } catch (_) {
                // caret placement is optional; typing still appends
            }
        }
        // Stop MathLive's bubble handler from preventDefault(). That cancel is
        // what makes Android Chrome drop the system keyboard after a tap.
        event.stopPropagation();
    };

    toggleMathKeypad = (event) => {
        event.preventDefault();
        event.stopPropagation();
        const field = this.mathFieldRef.current;
        const sink = field?.shadowRoot?.querySelector('.ML__keyboard-sink');
        const keypad = window.mathVirtualKeyboard;
        if (!field || !keypad) return;
        if (keypad.visible) {
            hideMathKeyboardAnimated();
            field.setAttribute('inputmode', 'decimal');
            if (sink) {
                sink.setAttribute('inputmode', 'decimal');
                try {
                    sink.focus({ preventScroll: true });
                } catch (err) {
                    field.focus();
                }
            }
            this.setState({ mathKeypad: false });
            return;
        }
        field.setAttribute('inputmode', 'none');
        if (sink) sink.setAttribute('inputmode', 'none');
        try {
            field.focus({ preventScroll: true });
        } catch (err) {
            field.focus();
        }
        showMathKeyboardAnimated();
        this.setState({ mathKeypad: true });
        window.setTimeout(this.keepFieldVisible, 80);
    };

    handleFocus = () => {
        if (this._blurHideTimer) {
            clearTimeout(this._blurHideTimer);
            this._blurHideTimer = null;
        }
        this.setState({ isMathFieldFocused: true });
    };

    handleBlur = () => {
        this.setState({ isMathFieldFocused: false });
    };

    handleMathFieldPointerUp = (event) => {
        const path = typeof event.composedPath === 'function' ? event.composedPath() : [];
        const isKeyboardToggle = path.some(
            (el) =>
                el?.classList?.contains?.('ML__virtual-keyboard-toggle') ||
                el?.getAttribute?.('part') === 'virtual-keyboard-toggle'
        );
        if (isKeyboardToggle) {
            if (window.mathVirtualKeyboard?.visible) {
                event.preventDefault();
                event.stopPropagation();
                hideMathKeyboardAnimated();
            } else if (!isMathKeyboardShowSuppressed()) {
                showMathKeyboardAnimated();
            }
            return;
        }
    };

    handleClickOutside = (event) => {
        if (!isMobileWidth(this.props.width)) return;
        if (!window.mathVirtualKeyboard?.visible) return;

        const mathField = this.mathFieldRef.current;
        const kbRoot = document.querySelector('.ML__keyboard');
        const path = typeof event.composedPath === 'function' ? event.composedPath() : [];
        const inKeyboard = path.some((el) => {
            const className = el?.className;
            const text = typeof className === 'string' ? className : '';
            return text.includes('ML__keyboard')
                || text.includes('MLK__')
                || text.includes('oat-math-kb-drag');
        }) || (kbRoot && kbRoot.contains(event.target));
        const inField = path.includes(mathField)
            || (mathField && (mathField === event.target || mathField.contains?.(event.target)));

        if (event.target?.closest?.('[data-math-keypad-toggle]')) return;

        if (!inKeyboard && !inField) {
            // Block later document listeners (MathLive) without killing the tap target's click.
            event.stopImmediatePropagation?.();
            hideMathKeyboardAnimated();
        }
    };

    isMatrixInput() {
        if (this.props.step?.stepAnswer) {
            return this.props.step?.problemType !== "MultipleChoice" &&
                /\\begin{[a-zA-Z]?matrix}/.test(this.props.step.stepAnswer[0])
        }
        if (this.props.step?.hintAnswer) {
            return this.props.step?.problemType !== "MultipleChoice" &&
                /\\begin{[a-zA-Z]?matrix}/.test(this.props.step.hintAnswer[0])
        }
    }

    onEquationChange(eq) {
        const containerEl = this.equationRef?.current
        const eqContentEl = this.equationRef?.current?.querySelector(".mq-editable-field")

        const textareaEl = this.equationRef?.current?.querySelector(".mq-textarea > textarea")

        if (textareaEl != null) {
            // console.debug("not null!", textareaEl)
            textareaEl.ariaLabel = `The current value is: ${eq}. Answer question number ${this.props.index} here.`
        }

        if (containerEl != null && eqContentEl != null) {
            const eqContainer = eqContentEl.querySelector("*[mathquill-block-id]")
            if (eqContainer != null) {
                const tallestEqElement = Math.max(...Array.from(eqContainer.childNodes.values()).map(el => el.offsetHeight))
                const newHeight = Math.max(tallestEqElement + 20, 50)

                containerEl.style.height = `${newHeight}px`;
                eqContainer.style.height = `${newHeight}px`;
            }
        }
        this.props.setInputValState(eq)
    }

    render() {
        const { classes, state, index, showCorrectness, allowRetry, variabilization, textBoxLayout, width } = this.props;
        const isMobile = isMobileWidth(width);
        const { use_expanded_view, debug } = this.context;
        let { problemType, stepAnswer, hintAnswer, units } = this.props.step;
        const keepMCOrder = this.props.keepMCOrder;

        const problemAttempted = state.isCorrect != null
        const correctAnswer = Array.isArray(stepAnswer) ? stepAnswer[0] : hintAnswer[0]
        const disableInput = problemAttempted && !allowRetry

        if (this.isMatrixInput()) {
            problemType = "MatrixInput"
        }

        const defaultLayout = {
            leftMd: 2,
            mainMd: 6,
            rightMd: 3,
        };
        const { leftMd, mainMd, rightMd } = {
            ...defaultLayout,
            ...(textBoxLayout || {}),
        };

        return (
            <Grid container spacing={0} justifyContent="flex-start" alignItems="center"
                className={clsx(disableInput && 'disable-interactions')}>
                <Grid item xs={false} md={problemType === "TextBox" ? leftMd : false}/>
                <Grid item xs={12} sm={isMobile ? 12 : 9} md={problemType === "TextBox" ? mainMd : 12}>
                    {(problemType === "TextBox" && this.props.step.answerType !== "string") && (
                        <>
                        <math-field
                            ref={(node) => {
                                this.mathFieldRef.current = node;
                                if (node) this.attachMathField();
                            }}
                            math-virtual-keyboard-policy={isMobile || wantsNativeKeyboard() ? "manual" : "sandboxed"}
                            inputMode={isMobile || wantsNativeKeyboard() ? "decimal" : undefined}
                            onFocus={this.handleFocus}
                            onBlur={this.handleBlur}
                            onPointerDown={this.handleMathFieldPointerDown}
                            onPointerUp={this.handleMathFieldPointerUp}
                            style={{ display: "block" }}
                            default-value={(use_expanded_view && debug) ? correctAnswer : (state.inputVal || "")}
                            autoCommands={EQUATION_EDITOR_AUTO_COMMANDS}
                            autoOperatorNames={EQUATION_EDITOR_AUTO_OPERATORS}
                        >
                        </math-field>
                        {(isMobile || wantsNativeKeyboard()) && (
                            <button
                                type="button"
                                data-math-keypad-toggle="true"
                                aria-pressed={Boolean(this.state.mathKeypad)}
                                onPointerDown={(event) => {
                                    if (event.button != null && event.button !== 0) return;
                                    // Keep focus on the answer field instead of the button,
                                    // or Android closes the keyboard.
                                    event.preventDefault();
                                    this.toggleMathKeypad(event);
                                }}
                                style={{
                                    marginTop: 8,
                                    minHeight: 44,
                                    padding: "8px 12px",
                                    borderRadius: 8,
                                    border: "1px solid #4F86A8",
                                    background: this.state.mathKeypad ? "#1f4b6e" : "#fff",
                                    color: this.state.mathKeypad ? "#fff" : "#1f4b6e",
                                    fontSize: 16,
                                }}
                            >
                                {this.state.mathKeypad ? "Native keyboard" : "Math keypad"}
                            </button>
                        )}
                        </>
                    )}               
                    {(problemType === "TextBox" && this.props.step.answerType === "string") && (
                        <TextField
                            inputProps={{
                                min: 0,
                                inputMode: "text",
                                autoComplete: "off",
                                autoCorrect: "off",
                                spellCheck: "false",
                                style: { textAlign: 'center', fontSize: 16 },
                                "aria-label": "Enter a response to the question above"
                            }}
                            onPointerDown={(event) => {
                                const input = event.currentTarget.querySelector?.('input, textarea')
                                    || (event.target?.matches?.('input, textarea') ? event.target : null);
                                if (input && document.activeElement !== input) input.focus({ preventScroll: true });
                            }}
                            {...stagingProp({
                                "data-selenium-target": `string-answer-${index}`
                            })}
                            error={showCorrectness && state.isCorrect === false}
                            className={classes.inputField}
                            variant="outlined"
                            onChange={(evt) => this.props.editInput(evt)}
                            onKeyPress={(evt) => this.props.handleKey(evt)}
                            InputProps={{
                                classes: {
                                    notchedOutline: ((showCorrectness && state.isCorrect !== false && state.usedHints) ? classes.muiUsedHint : null)
                                }
                            }}
                            {...(use_expanded_view && debug) ? {
                                defaultValue: correctAnswer
                            } : {}}
                        >
                        </TextField>
                    )}
                    {(problemType === "TextBox" && this.props.step.answerType === "short-essay") && (
                        <textarea
                            className="short-essay-input"
                            inputMode="text"
                            onPointerDown={(event) => {
                                if (document.activeElement !== event.currentTarget) {
                                    event.currentTarget.focus();
                                }
                            }}
                            onChange={(evt) => this.props.editInput(evt)}
                            onKeyPress={(evt) => this.props.handleKey(evt)}
                        >
                        </textarea>
                    )}
                                        {(problemType === "MultipleChoice" && keepMCOrder) ? (
                        <MultipleChoice
                            onChange={(evt) => this.props.editInput(evt)}
                            choices={[...this.props.step.choices].reverse()}
                            index={index}
                            {...(use_expanded_view && debug) ? {
                                defaultValue: correctAnswer
                            } : {}}
                            variabilization={variabilization}
                        />
                    ) :
                    (problemType === "MultipleChoice") && (
                        <MultipleChoice
                            onChange={(evt) => this.props.editInput(evt)}
                            choices={shuffleArray(this.props.step.choices, this.props.seed)}
                            index={index}
                            {...(use_expanded_view && debug) ? {
                                defaultValue: correctAnswer
                            } : {}}
                            variabilization={variabilization}
                        />
                    )}
                    {problemType === "GridInput" && (
                        <GridInput
                            onChange={(newVal) => this.props.setInputValState(newVal)}
                            numRows={this.props.step.numRows}
                            numCols={this.props.step.numCols}
                            context={this.props.context}
                            classes={this.props.classes}
                            index={index}
                            {...(use_expanded_view && debug) ? {
                                defaultValue: parseMatrixTex(correctAnswer)[0]
                            } : {}}
                        />
                    )}
                    {problemType === "MatrixInput" && (
                        <MatrixInput
                            onChange={(newVal) => this.props.setInputValState(newVal)}
                            numRows={this.props.step.numRows}
                            numCols={this.props.step.numCols}
                            context={this.props.context}
                            classes={this.props.classes}
                            index={index}
                            {...(use_expanded_view && debug) ? {
                                defaultValue: parseMatrixTex(correctAnswer)[0]
                            } : {}}
                        />
                    )}
                </Grid>
                {units && (
                <Grid item xs={12} sm={isMobile ? 12 : 2} md={1}>
                    <div style={{ marginLeft: isMobile ? 0 : "20%", marginTop: isMobile ? 4 : 0 }}>
                        {renderText(units, this.context.problemID, variabilization, this.context)}
                    </div>
                </Grid>
                )}
                <Grid item xs={false} md={problemType === "TextBox" ? rightMd : false}/>
            </Grid>
        )
    }
}

export default withWidth()(ProblemInput);
