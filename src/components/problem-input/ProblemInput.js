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
        field.dataset.oatBound = '1';
        this._mathField = field;
        this._onMathInput = () => this.publishMathValue(field);
        field.addEventListener('input', this._onMathInput);
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
     * Android Chrome / Gboard delivers text through beforeinput on the hidden
     * keyboard sink (often keyCode 229) and MathLive 0.109 sometimes drops it.
     * If the visible value did not change, insert the character ourselves.
     */
    bridgeAndroidIme = (field) => {
        const sink = field.shadowRoot?.querySelector('.ML__keyboard-sink');
        if (!sink || sink.dataset.oatIme === '1') return;
        sink.dataset.oatIme = '1';
        sink.setAttribute('enterkeyhint', 'done');
        sink.setAttribute('autocapitalize', 'off');

        const syncInputMode = () => {
            const virtualOpen = Boolean(window.mathVirtualKeyboard?.visible);
            sink.setAttribute('inputmode', virtualOpen ? 'none' : 'text');
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
        const viewport = window.visualViewport;
        const visibleTop = viewport ? viewport.offsetTop : 0;
        const visibleBottom = viewport
            ? viewport.offsetTop + viewport.height
            : window.innerHeight;
        const keyboard = document.querySelector('body > .ML__keyboard.is-visible .MLK__backdrop');
        const keyboardTop = keyboard ? keyboard.getBoundingClientRect().top : visibleBottom;
        const limit = Math.min(visibleBottom, keyboardTop) - 12;
        const rect = field.getBoundingClientRect();
        if (rect.bottom > limit || rect.top < visibleTop + 64) {
            const delta = rect.bottom - limit + 28;
            window.scrollBy({ top: delta, left: 0, behavior: 'smooth' });
        }
    };

    handleKeyboardVisibility = (event) => {
        if (this._syncImeMode) this._syncImeMode();
        if (event?.detail?.open) {
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

    /** Mobile: open MathLive keyboard when the field is interacted with and it's hidden. */
    showMobileKeyboardIfNeeded = () => {
        if (!isMobileWidth(this.props.width)) return;
        if (isMathKeyboardShowSuppressed()) return;
        const mathField = this.mathFieldRef.current;
        if (!mathField) return;
        if (window.mathVirtualKeyboard?.visible) return;
        try {
            mathField.focus?.();
        } catch (e) {
            // ignore
        }
        showMathKeyboardAnimated();
    };

    handleFocus = () => {
        if (this._blurHideTimer) {
            clearTimeout(this._blurHideTimer);
            this._blurHideTimer = null;
        }
        this.setState({ isMathFieldFocused: true });
        // manual policy: we open explicitly; still guard against dismiss races
        if (!isMathKeyboardShowSuppressed()) {
            this.showMobileKeyboardIfNeeded();
        }
        window.setTimeout(this.keepFieldVisible, 50);
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
        this.showMobileKeyboardIfNeeded();
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
                        <math-field
                            ref={(node) => {
                                this.mathFieldRef.current = node;
                                if (node) this.attachMathField();
                            }}
                            math-virtual-keyboard-policy={isMobile ? "manual" : "sandboxed"}
                            onFocus={this.handleFocus}
                            onBlur={this.handleBlur}
                            onPointerUp={this.handleMathFieldPointerUp}
                            style={{ display: "block" }}
                            default-value={(use_expanded_view && debug) ? correctAnswer : (state.inputVal || "")}
                            autoCommands={EQUATION_EDITOR_AUTO_COMMANDS}
                            autoOperatorNames={EQUATION_EDITOR_AUTO_OPERATORS}
                        >
                        </math-field>
                    )}               
                    {(problemType === "TextBox" && this.props.step.answerType === "string") && (
                        <TextField
                            ref={this.textFieldRef}
                            inputProps={{
                                min: 0,
                                inputMode: "text",
                                autoComplete: "off",
                                autoCorrect: "off",
                                spellCheck: "false",
                                style: { textAlign: 'center', fontSize: 16 },
                                "aria-label": "Enter a response to the question above"
                            }}
                            onFocus={(event) => {
                                event.target.scrollIntoView({ block: 'center', inline: 'nearest' });
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
