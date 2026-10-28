import React, { useEffect, useRef, useState } from "react";
import { useHistory } from "react-router-dom";
import Button from "@material-ui/core/Button";
import ProblemWrapper from "../problem-layout/ProblemWrapper";
import { loadProblemPool } from "../../content/loadProblemPool";
import {
    ALGEBRA_CHECK_PROBLEMS,
} from "../../course-gate/algebraCheckProblems";
import {
    PASS_RATIO,
    isAdvancedUnlocked,
    passedAlgebraCheck,
    readUnlockRecord,
    writeUnlock,
} from "../../course-gate/courseAccess";

const LESSON = {
    id: "algebra-check",
    name: "Algebra Check",
    topics: "Elementary algebra placement",
    courseName: "Algebra Check",
    courseOER: "https://openstax.org/details/books/elementary-algebra-2e <OpenStax: Elementary Algebra>",
    courseLicense: "https://creativecommons.org/licenses/by/4.0/ <CC BY 4.0>",
    learningObjectives: { review: 0.85 },
    doMasteryUpdate: false,
    giveStuHints: true,
    giveStuFeedback: true,
    allowRecycle: false,
    allowBottomHint: true,
    allowDynamicHint: false,
    allowTTS: false,
    guidedHints: false,
};

function neededCorrect(total) {
    return Math.ceil(total * PASS_RATIO - 1e-9);
}

export default function AlgebraCheck() {
    const history = useHistory();
    const [phase, setPhase] = useState("loading");
    const [problems, setProblems] = useState([]);
    const [missing, setMissing] = useState([]);
    const [index, setIndex] = useState(0);
    const [results, setResults] = useState([]);
    const [error, setError] = useState("");
    const [alreadyUnlocked] = useState(() => isAdvancedUnlocked());
    const attemptRef = useRef({ seen: 0, clean: true });

    useEffect(() => {
        let cancelled = false;
        loadProblemPool()
            .then((pool) => {
                if (cancelled) return;
                const byId = new Map(pool.map((problem) => [problem.id, problem]));
                const found = [];
                const absent = [];
                ALGEBRA_CHECK_PROBLEMS.forEach((item) => {
                    const problem = byId.get(item.id);
                    if (problem) found.push({ ...item, problem });
                    else absent.push(item);
                });
                setProblems(found);
                setMissing(absent);
                setPhase(found.length >= 15 ? "intro" : "error");
                if (found.length < 15) {
                    setError("The Algebra Check problems are not in the loaded course content.");
                }
            })
            .catch((err) => {
                if (cancelled) return;
                setError(err.message || "Could not load problems.");
                setPhase("error");
            });
        return () => {
            cancelled = true;
        };
    }, []);

    const total = problems.length;
    const need = neededCorrect(total);
    const correctCount = results.filter((item) => item.correct).length;

    const onStepAttempt = ({ isCorrect, helpUsed }) => {
        attemptRef.current.seen += 1;
        if (!isCorrect || helpUsed) attemptRef.current.clean = false;
    };

    const finishProblem = async () => {
        const current = problems[index];
        const steps = current.problem.steps?.length || 1;
        const attempt = attemptRef.current;
        const correct = attempt.clean && attempt.seen >= steps;
        const nextResults = [
            ...results,
            {
                id: current.id,
                topic: current.topic,
                review: current.review,
                correct,
            },
        ];
        if (index + 1 >= problems.length) {
            const correctTotal = nextResults.filter((item) => item.correct).length;
            if (passedAlgebraCheck(correctTotal, nextResults.length)) {
                writeUnlock({
                    source: "algebra-check",
                    correct: correctTotal,
                    total: nextResults.length,
                    score: correctTotal / nextResults.length,
                });
            }
            setResults(nextResults);
            setPhase("results");
            return;
        }
        attemptRef.current = { seen: 0, clean: true };
        setResults(nextResults);
        setIndex(index + 1);
    };

    const restart = () => {
        attemptRef.current = { seen: 0, clean: true };
        setResults([]);
        setIndex(0);
        setPhase("question");
    };

    const shell = (children) => (
        <div style={{ background: "#F6F6F6", minHeight: "100vh", padding: "24px 16px 48px" }}>
            <div style={{ maxWidth: 880, margin: "0 auto" }}>{children}</div>
        </div>
    );

    if (phase === "loading") {
        return shell(<h1 style={{ fontSize: 28 }}>Loading the Algebra Check…</h1>);
    }

    if (phase === "error") {
        return shell(
            <>
                <h1 style={{ fontSize: 28 }}>Algebra Check</h1>
                <p>{error}</p>
                <Button variant="contained" color="primary" onClick={() => history.push("/")}>
                    Back to courses
                </Button>
            </>
        );
    }

    if (phase === "intro") {
        return shell(
            <>
                <h1 style={{ fontSize: 32, marginBottom: 8 }}>Algebra Check</h1>
                <p style={{ fontSize: 18, lineHeight: 1.5 }}>
                    {total} problems from Elementary Algebra, one each from the main topics.
                    Score at least {need} correct ({Math.round(PASS_RATIO * 100)}%) to unlock
                    every course beyond Pre-Algebra and Elementary Algebra.
                </p>
                <p style={{ fontSize: 16, lineHeight: 1.5 }}>
                    A problem counts only if every part is right on the first try and you
                    do not open a hint. Hints still work, and they walk through the method,
                    but using one marks that problem as not yet solid. You can retake the
                    check. A lower score later will not lock courses again.
                </p>
                {alreadyUnlocked && (
                    <p style={{ fontSize: 16 }}>
                        Advanced courses are already unlocked on this browser
                        {readUnlockRecord()?.source === "elementary-mastery"
                            ? " because Elementary Algebra is mastered."
                            : "."}
                    </p>
                )}
                {missing.length > 0 && (
                    <p style={{ fontSize: 14, color: "#666" }}>
                        {missing.length} planned {missing.length === 1 ? "problem is" : "problems are"} missing
                        from this content version and {missing.length === 1 ? "was" : "were"} left out.
                    </p>
                )}
                <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginTop: 16 }}>
                    <Button variant="contained" color="primary" onClick={() => setPhase("question")}>
                        Start
                    </Button>
                    <Button variant="outlined" color="primary" onClick={() => history.push("/")}>
                        Back to courses
                    </Button>
                </div>
            </>
        );
    }

    if (phase === "results") {
        const passed = passedAlgebraCheck(correctCount, results.length);
        const missed = results.filter((item) => !item.correct);
        return shell(
            <>
                <h1 style={{ fontSize: 32 }}>{passed ? "You passed." : "Not yet."}</h1>
                <p style={{ fontSize: 20 }}>
                    {correctCount} of {results.length} correct ({Math.round((correctCount / results.length) * 100)}%).
                    The bar is {need} of {results.length}.
                </p>
                {passed ? (
                    <p style={{ fontSize: 16, lineHeight: 1.5 }}>
                        Advanced courses are unlocked on this browser. Pre-Algebra and Elementary
                        Algebra stay available either way. If a later course feels shaky, come back
                        to the matching Elementary Algebra lesson. Mastery there is saved on this device.
                    </p>
                ) : (
                    <p style={{ fontSize: 16, lineHeight: 1.5 }}>
                        The misses below are the topics to practice before you try again.
                        Work the Elementary Algebra lesson for that topic, and use the hints:
                        they are there to show the method, not just the final number.
                    </p>
                )}
                {missed.length > 0 && (
                    <ul style={{ paddingLeft: 20, fontSize: 16, lineHeight: 1.45 }}>
                        {missed.map((item) => (
                            <li key={item.id} style={{ marginBottom: 10 }}>
                                <strong>{item.topic}.</strong> {item.review}
                            </li>
                        ))}
                    </ul>
                )}
                <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginTop: 16 }}>
                    <Button variant="contained" color="primary" onClick={() => history.push("/")}>
                        {passed ? "See unlocked courses" : "Back to courses"}
                    </Button>
                    <Button variant="outlined" color="primary" onClick={restart}>
                        Try the check again
                    </Button>
                </div>
            </>
        );
    }

    const current = problems[index];
    return shell(
        <>
            <div style={{ display: "flex", justifyContent: "space-between", gap: 12, alignItems: "baseline", flexWrap: "wrap" }}>
                <h1 style={{ fontSize: 22, margin: "0 0 8px" }}>
                    Algebra Check · {index + 1} of {total}
                </h1>
                <Button size="small" onClick={() => history.push("/")}>Exit</Button>
            </div>
            <p style={{ marginTop: 0, color: "#444" }}>{current.topic}</p>
            <ProblemWrapper
                key={`${current.id}-${index}-${results.length}`}
                problem={current.problem}
                problemComplete={finishProblem}
                lesson={LESSON}
                seed={String(index + 1)}
                lessonID="algebra-check"
                displayMastery={() => {}}
                onStepAttempt={onStepAttempt}
                nextButtonLabel={index + 1 === total ? "See results" : "Next problem"}
            />
        </>
    );
}
