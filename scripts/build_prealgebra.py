#!/usr/bin/env python3
"""Build the Pre-Algebra course in OATutor's native content format.

Problems are original (OpenStax Prealgebra 2e topics, not textbook wording).
Every numeric answer is computed from a Python expression and checked again
when the JSON is read back. Hint sequences teach the method:

1. A scaffold that names the idea and asks a guiding question.
2. Further scaffolds that check each step of the method.
3. A final plain-language worked solution with a reusable general rule.

The final hint is type "hint" (read after the scaffolds), not an immediate
answer reveal.
"""

from __future__ import annotations

import json
import os
import re
import shutil
from decimal import Decimal
from fractions import Fraction

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "src", "local-content", "prealgebra")
POOL = os.path.join(OUT, "content-pool")

OER = (
    "https://openstax.org/details/books/prealgebra-2e "
    "<OpenStax Prealgebra 2e; original exercises, CC BY 4.0>"
)
LICENSE = "https://creativecommons.org/licenses/by/4.0/ <CC BY 4.0>"
SAFE = {"Fraction": Fraction, "Decimal": Decimal}


def ev(expr):
    if isinstance(expr, (int, Fraction, Decimal)):
        return expr
    return eval(expr, {"__builtins__": {}}, SAFE)


def same(a, b):
    if isinstance(a, Decimal) or isinstance(b, Decimal):
        return Decimal(str(a)) == Decimal(str(b))
    return Fraction(a) == Fraction(b)


def latex_of(value):
    if isinstance(value, str):
        return value
    if isinstance(value, Decimal):
        text = format(value, "f")
        if "." in text:
            text = text.rstrip("0").rstrip(".")
        return f"$${text}$$"
    if isinstance(value, float):
        raise TypeError("use Decimal or Fraction, not float")
    frac = Fraction(value)
    if frac.denominator == 1:
        return f"$${frac.numerator}$$"
    sign = "-" if frac < 0 else ""
    mag = abs(frac)
    return f"$${sign}\\frac{{{mag.numerator}}}{{{mag.denominator}}}$$"


def parse_latex(tex):
    raw = tex.strip()
    if raw.startswith("$$") and raw.endswith("$$"):
        raw = raw[2:-2]
    raw = raw.replace(" ", "")
    if re.fullmatch(r"-?\\frac\{\d+\}\{\d+\}", raw):
        sign = -1 if raw.startswith("-") else 1
        num, den = re.findall(r"\d+", raw)
        return Fraction(sign * int(num), int(den))
    if re.fullmatch(r"-?\d+(?:\.\d+)?", raw):
        if "." in raw:
            return Decimal(raw)
        return Fraction(int(raw), 1)
    return raw


class StepBuilder:
    def __init__(self, kc, prompt, answer_expr):
        self.kc = kc
        self.prompt = _norm(prompt)
        self.answer = ev(answer_expr)
        self.hints = []

    def guide(self, title, text, expr=None, choices=None, choice=None):
        self.hints.append(_scaffold(title, text, expr, choices, choice))
        return self

    def check(self, title, text, expr):
        self.hints.append(_scaffold(title, text, expr, None, None))
        return self

    def worked(self, text):
        text = _norm(text)
        if "General rule:" not in text:
            raise AssertionError("worked solution needs a 'General rule:' line")
        if "common mistake" not in text.lower():
            raise AssertionError("worked solution should name a common mistake")
        self.hints.append(
            {
                "type": "hint",
                "title": "Worked solution",
                "text": text,
            }
        )
        return self

    def done(self):
        if len(self.hints) < 3:
            raise AssertionError(f"need at least 3 hints for: {self.prompt}")
        if self.hints[0]["type"] != "scaffold":
            raise AssertionError("first hint must be a guiding scaffold")
        if self.hints[-1]["type"] != "hint":
            raise AssertionError("last hint must be the worked solution")
        if not any(h["type"] == "scaffold" for h in self.hints[1:-1]):
            raise AssertionError("need a middle scaffold that checks a step")
        first = self.hints[0]
        if first.get("answerType") == "arithmetic" and same(first["_value"], self.answer):
            raise AssertionError(f"guiding question gives away the final answer: {self.prompt}")
        # At least one scaffold must be an intermediate, not the final result.
        intermediates = [
            h
            for h in self.hints
            if h["type"] == "scaffold" and h.get("answerType") == "arithmetic" and not same(h["_value"], self.answer)
        ]
        if not intermediates and first.get("answerType") != "string":
            raise AssertionError("no intermediate check before the final value")
        return {
            "kc": self.kc,
            "prompt": self.prompt,
            "answer": self.answer,
            "hints": self.hints,
        }


def _norm(text):
    # Authoring sometimes doubled backslashes. LaTeX in the app wants one.
    return text.replace("\\\\", "\\")


def _scaffold(title, text, expr, choices, choice):
    text = _norm(text)
    title = _norm(title)
    if choices is not None:
        if choice not in choices:
            raise AssertionError(f"choice {choice!r} not in {choices}")
        return {
            "type": "scaffold",
            "title": title,
            "text": text,
            "problemType": "MultipleChoice",
            "answerType": "string",
            "choices": list(choices),
            "hintAnswer": [choice],
        }
    value = ev(expr)
    return {
        "type": "scaffold",
        "title": title,
        "text": text,
        "problemType": "TextBox",
        "answerType": "arithmetic",
        "hintAnswer": [latex_of(value)],
        "_value": value,
    }


def step(kc, prompt, answer_expr):
    return StepBuilder(kc, prompt, answer_expr)


def problem(title, body, steps):
    built = [s.done() if isinstance(s, StepBuilder) else s for s in steps]
    return {"title": title, "body": body, "steps": built}


def lesson(number, name, topics, objectives, problems):
    return {
        "number": number,
        "name": name,
        "topics": topics,
        "objectives": objectives,
        "problems": problems,
    }


def lessons():
    L = []
    ops = "prealg_order_of_operations"
    whole = "prealg_whole_number_operations"
    L.append(
        lesson(
            1,
            "1. Whole Numbers and Order of Operations",
            "Whole numbers and order of operations",
            [ops, whole],
            [
                problem(
                    "Multiplication before addition",
                    "Evaluate each expression. Do not work strictly left to right unless the operations have the same priority.",
                    [
                        step(ops, r"$$6 + 4 \times 5$$", "6 + 4 * 5")
                        .guide(
                            "Which operation comes first?",
                            "Order of operations: multiplication and division are done before addition and subtraction, unless parentheses say otherwise. A common mistake is to add $$6 + 4$$ first just because those numbers are written on the left. In $$6 + 4 \\times 5$$, which operation do you do first?",
                            choices=["Addition", "Multiplication"],
                            choice="Multiplication",
                        )
                        .check(
                            "Compute the product",
                            "The factor pair that must be combined first is $$4 \\times 5$$. That product is what you will add to 6. What is $$4 \\times 5$$?",
                            "4 * 5",
                        )
                        .check(
                            "Add the remaining term",
                            "The expression is now $$6$$ plus that product. Addition is the lower-priority operation, so it happens second. What is $$6 + 20$$?",
                            "6 + 20",
                        )
                        .worked(
                            "$$6 + 4 \\times 5 = 6 + 20 = 26$$. Common mistake: adding $$6 + 4$$ first to get $$10 \\times 5 = 50$$. General rule: when multiplication and addition are both present, multiply first, then add."
                        ),
                        step(whole, r"$$(8 + 2) \times 3$$", "(8 + 2) * 3")
                        .guide(
                            "What do parentheses change?",
                            "Parentheses are a grouping symbol: finish the inside before you use the result outside. A common mistake is to multiply $$2 \\times 3$$ first and ignore the parentheses. What is $$8 + 2$$, the value inside the parentheses?",
                            "8 + 2",
                        )
                        .check(
                            "Use that result as a factor",
                            "The parentheses are now a single factor of 10. Multiplication is next. What is $$10 \\times 3$$?",
                            "10 * 3",
                        )
                        .worked(
                            "$$(8 + 2) \\times 3 = 10 \\times 3 = 30$$. Common mistake: multiplying before adding inside the parentheses, which gives $$8 + 6 = 14$$. General rule: evaluate inside parentheses first, then use that number in the remaining expression."
                        ),
                    ],
                ),
                problem(
                    "Several operations in one expression",
                    "Evaluate each expression. Division and multiplication are done before addition, and from left to right when they share that priority.",
                    [
                        step(ops, r"$$48 \div 6 + 3 \times 2$$", "48 // 6 + 3 * 2")
                        .guide(
                            "Which pieces are not addition?",
                            "Addition waits until multiplication and division are finished. There are two higher-priority pieces here: $$48 \\div 6$$ and $$3 \\times 2$$. A common mistake is to do $$6 + 3$$ because those numbers sit next to each other. What is $$48 \\div 6$$?",
                            "48 // 6",
                        )
                        .check(
                            "Compute the product",
                            "The other higher-priority piece is independent of the division. What is $$3 \\times 2$$?",
                            "3 * 2",
                        )
                        .check(
                            "Add the two results",
                            "The expression has collapsed to $$8 + 6$$. What is that sum?",
                            "8 + 6",
                        )
                        .worked(
                            "$$48 \\div 6 + 3 \\times 2 = 8 + 6 = 14$$. Common mistake: adding $$6 + 3$$ before multiplying or dividing. General rule: finish every multiplication and division, then do the addition."
                        ),
                        step(ops, r"$$100 - 4 \\times (3 + 5)$$", "100 - 4 * (3 + 5)")
                        .guide(
                            "Where do you start?",
                            "Parentheses outrank multiplication, and multiplication outranks subtraction. A common mistake is to subtract $$100 - 4$$ first. What is $$3 + 5$$, inside the parentheses?",
                            "3 + 5",
                        )
                        .check(
                            "Multiply by the factor outside",
                            "The 4 is a factor on the whole group, so it multiplies the 8 you just found. What is $$4 \\times 8$$?",
                            "4 * 8",
                        )
                        .check(
                            "Subtract from 100",
                            "The expression is now $$100 - 32$$. Subtraction is last. What is $$100 - 32$$?",
                            "100 - 32",
                        )
                        .worked(
                            "$$100 - 4 \\times (3 + 5) = 100 - 4 \\times 8 = 100 - 32 = 68$$. Common mistake: subtracting before multiplying, or multiplying only the 3 by 4. General rule: parentheses, then multiplication, then subtraction."
                        ),
                    ],
                ),
                problem(
                    "Same priority, left to right",
                    "Multiplication and division have the same priority. So do addition and subtraction. Work those pairs from left to right.",
                    [
                        step(ops, r"$$18 \\div 3 \\times 2$$", "(18 // 3) * 2")
                        .guide(
                            "Left to right, or the times sign first?",
                            "Division and multiplication are the same priority, so the left one happens first. A common mistake is to multiply $$3 \\times 2$$ first and then divide 18 by 6. What is $$18 \\div 3$$?",
                            "18 // 3",
                        )
                        .check(
                            "Then multiply",
                            "You now have $$6 \\times 2$$. What is that product?",
                            "6 * 2",
                        )
                        .worked(
                            "$$18 \\div 3 \\times 2 = 6 \\times 2 = 12$$. Common mistake: treating the expression as $$18 \\div (3 \\times 2) = 3$$. General rule: multiplication and division are done left to right, not 'multiplication always before division.'"
                        ),
                        step(whole, r"$$7 \\times 8 + 6 \\times 5$$", "7 * 8 + 6 * 5")
                        .guide(
                            "How many products are there?",
                            "Each multiplication is its own higher-priority piece. A common mistake is to add $$8 + 6$$ because they are in the middle. What is $$7 \\times 8$$?",
                            "7 * 8",
                        )
                        .check(
                            "Second product",
                            "The other product does not use the 56 you just found. What is $$6 \\times 5$$?",
                            "6 * 5",
                        )
                        .check(
                            "Add the products",
                            "Now add those two results. What is $$56 + 30$$?",
                            "56 + 30",
                        )
                        .worked(
                            "$$7 \\times 8 + 6 \\times 5 = 56 + 30 = 86$$. Common mistake: adding $$8 + 6$$ first. General rule: compute each product, then add the products."
                        ),
                    ],
                ),
                problem(
                    "Place value in multi-digit arithmetic",
                    "These use only whole numbers. Keep track of place value: tens are worth ten times as much as ones.",
                    [
                        step(whole, r"$$46 \\times 20$$", "46 * 20")
                        .guide(
                            "What does the trailing zero tell you?",
                            "$$20 = 2 \\times 10$$. Multiplying by 10 shifts every digit one place to the left (append a zero). A common mistake is to multiply $$46 \\times 2$$ and forget to account for the ten. What is $$46 \\times 2$$?",
                            "46 * 2",
                        )
                        .check(
                            "Attach the factor of 10",
                            "Multiplying 92 by 10 moves 92 into the tens. What is $$92 \\times 10$$?",
                            "92 * 10",
                        )
                        .worked(
                            "$$46 \\times 20 = 46 \\times 2 \\times 10 = 92 \\times 10 = 920$$. Common mistake: writing 92, or writing 9200 because both factors 'look like' they add a zero. General rule: separate the trailing zeros, multiply the remaining whole numbers, then put the zeros back."
                        ),
                        step(whole, r"$$735 \\div 5$$", "735 // 5")
                        .guide(
                            "Split the dividend by place value",
                            "$$735 = 700 + 35$$, and both parts are divisible by 5. A common mistake is to divide only 35 and forget the hundreds. What is $$700 \\div 5$$?",
                            "700 // 5",
                        )
                        .check(
                            "Divide the rest",
                            "What is $$35 \\div 5$$?",
                            "35 // 5",
                        )
                        .check(
                            "Add the partial quotients",
                            "The quotient is $$140 + 7$$. What is that sum?",
                            "140 + 7",
                        )
                        .worked(
                            "$$735 \\div 5 = 700 \\div 5 + 35 \\div 5 = 140 + 7 = 147$$. Check: $$147 \\times 5 = 735$$. Common mistake: dividing digit by digit without place value and getting 117 or 17. General rule: you can split a dividend into parts that divide evenly, divide each part, and add the quotients."
                        ),
                    ],
                ),
            ],
        )
    )

    add = "prealg_integer_add_sub"
    mul = "prealg_integer_mul_div"
    L.append(
        lesson(
            2,
            "2. Integers and Negative Numbers",
            "Integers and negative numbers",
            [add, mul],
            [
                problem(
                    "Adding and subtracting signed numbers",
                    "The sign tells direction on the number line: positive to the right, negative to the left.",
                    [
                        step(add, r"$$-8 + 15$$", "-8 + 15")
                        .guide(
                            "Same sign or opposite signs?",
                            "Adding a positive number moves right. You start at $$-8$$ and move 15 units right. A common mistake is to add the absolute values and keep the negative sign. Which way does $$+15$$ move you?",
                            choices=["Left, toward more negative", "Right, toward positive"],
                            choice="Right, toward positive",
                        )
                        .check(
                            "How far past zero?",
                            "The first 8 units of the move cancel the debt of 8 and land on 0. The remaining distance is $$15 - 8$$. What is $$15 - 8$$?",
                            "15 - 8",
                        )
                        .worked(
                            "$$-8 + 15 = 7$$. You move from $$-8$$ through 0 and 7 units into the positives. Common mistake: computing $$-(8 + 15) = -23$$. General rule: to add numbers with opposite signs, subtract the smaller absolute value from the larger one and keep the sign of the number with the larger absolute value."
                        ),
                        step(add, r"$$-12 - (-5)$$", "-12 - (-5)")
                        .guide(
                            "What does subtracting a negative mean?",
                            "Subtracting a number means adding its opposite. The opposite of $$-5$$ is positive 5, so this is not the same as $$-12 - 5$$. A common mistake is to move further left and answer $$-17$$. Subtracting $$-5$$ is the same as which operation?",
                            choices=["Adding positive 5", "Subtracting positive 5"],
                            choice="Adding positive 5",
                        )
                        .check(
                            "Rewrite, then add",
                            "The expression is now $$-12 + 5$$. The signs are opposite and 12 is larger, so the result stays negative. The distance that remains is $$12 - 5$$. What is $$12 - 5$$?",
                            "12 - 5",
                        )
                        .worked(
                            "$$-12 - (-5) = -12 + 5 = -7$$. Common mistake: $$ -12 - 5 = -17 $$, which subtracts a positive instead of a negative. General rule: $$a - (-b) = a + b$$. Subtracting a negative moves you in the positive direction."
                        ),
                    ],
                ),
                problem(
                    "Multiplying and dividing signed numbers",
                    "The product or quotient of two numbers with the same sign is positive. Opposite signs give a negative result.",
                    [
                        step(mul, r"$$-6 \\times 4$$", "-6 * 4")
                        .guide(
                            "What sign should the product have?",
                            "One factor is negative and one is positive, so the signs are opposite. A common mistake is to multiply the absolute values and leave the product positive. What sign does $$-6 \\times 4$$ have?",
                            choices=["Positive", "Negative"],
                            choice="Negative",
                        )
                        .check(
                            "Multiply the absolute values",
                            "Ignore the signs for a moment. What is $$6 \\times 4$$?",
                            "6 * 4",
                        )
                        .worked(
                            "$$-6 \\times 4 = -24$$. Common mistake: writing $$24$$ because 'times makes things bigger.' Size and sign are separate: the absolute value is 24, and opposite signs make it negative. General rule: opposite signs give a negative product; same signs give a positive product."
                        ),
                        step(mul, r"$$-36 \\div (-9)$$", "(-36) // (-9)")
                        .guide(
                            "Same signs or opposite signs?",
                            "Both the dividend and the divisor are negative, so the signs match. A common mistake is to think every expression that contains a minus sign has a negative answer. What sign does $$-36 \\div (-9)$$ have?",
                            choices=["Positive", "Negative"],
                            choice="Positive",
                        )
                        .check(
                            "Divide the absolute values",
                            "What is $$36 \\div 9$$?",
                            "36 // 9",
                        )
                        .worked(
                            "$$-36 \\div (-9) = 4$$. Check: $$-9 \\times 4 = -36$$. Common mistake: answering $$-4$$. General rule: the sign rule for division is the same as for multiplication. Two negatives make a positive."
                        ),
                    ],
                ),
                problem(
                    "Exponents and a leading minus sign",
                    "An exponent applies only to the number it is written on, unless parentheses include the sign.",
                    [
                        step(mul, r"$$(-3)^{2}$$", "(-3) ** 2")
                        .guide(
                            "Is the sign inside the base?",
                            "The parentheses include the minus sign in the base, so you multiply $$-3$$ by $$-3$$. A common mistake is to square only the 3 and then make the answer negative. Two negative factors have which kind of product?",
                            choices=["Positive", "Negative"],
                            choice="Positive",
                        )
                        .check(
                            "Multiply the absolute values",
                            "The sign is settled. What is $$3 \\times 3$$?",
                            "3 * 3",
                        )
                        .worked(
                            "$$(-3)^{2} = (-3) \\times (-3) = 9$$. Common mistake: answering $$-9$$, which is the value of $$-3^{2}$$ without parentheses. General rule: a negative base in parentheses, raised to an even power, is positive, because the minus signs pair up."
                        ),
                        step(mul, r"$$-3^{2}$$", "-(3 ** 2)")
                        .guide(
                            "What is the base of the exponent?",
                            "Without parentheses, the exponent binds only to the 3. The expression means 'the opposite of $$3^{2}$$,' not '$$(-3)$$ squared.' A common mistake is to treat this as identical to $$(-3)^{2}$$. What is $$3^{2}$$?",
                            "3 ** 2",
                        )
                        .check(
                            "Apply the leading minus",
                            "The minus is applied after the exponent. What is the opposite of 9?",
                            "-9",
                        )
                        .worked(
                            "$$-3^{2} = -(3^{2}) = -9$$. Common mistake: squaring $$-3$$ and answering $$9$$. General rule: $$-a^{n}$$ means $$-(a^{n})$$. Use parentheses, $$(-a)^{n}$$, when the sign is part of the base."
                        ),
                    ],
                ),
                problem(
                    "More signed arithmetic",
                    "Decide the sign from the operation, then compute the distance.",
                    [
                        step(add, r"$$7 - 18$$", "7 - 18")
                        .guide(
                            "Which direction wins?",
                            "$$7 - 18$$ means start at 7 and move 18 units left. You pass 0, so the result is negative. A common mistake is to answer $$11$$, the distance, and drop the sign. How far is 18 from 7? That is, what is $$18 - 7$$?",
                            "18 - 7",
                        )
                        .check(
                            "Attach the sign",
                            "The larger absolute value belongs to the negative term in $$7 + (-18)$$, so take the opposite of the distance 11. What signed number has absolute value 11 and is negative?",
                            "-11",
                        )
                        .worked(
                            "$$7 - 18 = -11$$. Common mistake: answering $$11$$. General rule: if you subtract a larger positive from a smaller positive, the result is negative, and the size of the result is the difference of the absolute values."
                        ),
                        step(mul, r"$$-4 \\times (-8)$$", "(-4) * (-8)")
                        .guide(
                            "What sign does the product have?",
                            "Both factors are negative, so the signs match. A common mistake is to keep a minus sign in the product. What sign should $$-4 \\times (-8)$$ have?",
                            choices=["Positive", "Negative"],
                            choice="Positive",
                        )
                        .check(
                            "Multiply the absolute values",
                            "What is $$4 \\times 8$$?",
                            "4 * 8",
                        )
                        .worked(
                            "$$-4 \\times (-8) = 32$$. Common mistake: answering $$-32$$. General rule: a negative times a negative is positive. You can check by noting that multiplying by $$-1$$ flips the sign, and flipping twice returns you to positive."
                        ),
                    ],
                ),
            ],
        )
    )
    import importlib.util
    rest_path = os.path.join(os.path.dirname(__file__), "prealgebra_rest.py")
    spec = importlib.util.spec_from_file_location("prealgebra_rest", rest_path)
    rest = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rest)
    rest.add_more(L, step, problem, lesson)
    return L


def _write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(obj, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def _hint_record(base_id, index, hint, previous_id):
    record = {
        "id": f"{base_id}-h{index}",
        "type": hint["type"],
        "title": hint["title"],
        "text": hint["text"],
        "dependencies": [] if previous_id is None else [previous_id],
        "variabilization": {},
        "oer": OER,
        "license": LICENSE,
    }
    if hint["type"] == "scaffold":
        record["problemType"] = hint["problemType"]
        record["answerType"] = hint["answerType"]
        record["hintAnswer"] = hint["hintAnswer"]
        if hint.get("choices"):
            record["choices"] = hint["choices"]
    return record


def emit(built_lessons):
    if os.path.isdir(POOL):
        shutil.rmtree(POOL)
    os.makedirs(POOL, exist_ok=True)

    course_lessons = []
    skill_model = {}
    bkt = {}
    answer_rows = []

    for lesson_spec in built_lessons:
        lesson_id = f"prealg-lesson-{lesson_spec['number']}"
        for kc in lesson_spec["objectives"]:
            bkt[kc] = {
                "probMastery": 0.1,
                "probTransit": 0.1,
                "probSlip": 0.1,
                "probGuess": 0.1,
            }
        course_lessons.append(
            {
                "id": lesson_id,
                "name": lesson_spec["name"],
                "topics": lesson_spec["topics"],
                "allowRecycle": True,
                "guidedHints": True,
                "allowBottomHint": False,
                "allowDynamicHint": False,
                "allowTTS": False,
                "learningObjectives": {kc: 0.85 for kc in lesson_spec["objectives"]},
            }
        )
        for p_index, prob in enumerate(lesson_spec["problems"], start=1):
            prob_id = f"prealg-l{lesson_spec['number']}p{p_index}"
            prob_dir = os.path.join(POOL, prob_id)
            steps_out = []
            for s_index, step_spec in enumerate(prob["steps"]):
                suffix = chr(ord("a") + s_index)
                step_id = f"{prob_id}{suffix}"
                skill_model[step_id] = [step_spec["kc"]]
                hint_dir_ids = []
                previous = None
                hint_records = []
                for h_index, hint in enumerate(step_spec["hints"], start=1):
                    record = _hint_record(step_id, h_index, hint, previous)
                    hint_records.append(record)
                    previous = record["id"]
                    if hint["type"] == "scaffold" and hint["answerType"] == "arithmetic":
                        parsed = parse_latex(hint["hintAnswer"][0])
                        if not same(parsed, hint["_value"]):
                            raise AssertionError(
                                f"{step_id} hint {h_index} latex {hint['hintAnswer'][0]} != {hint['_value']}"
                            )
                answer_latex = latex_of(step_spec["answer"])
                parsed_answer = parse_latex(answer_latex)
                if not same(parsed_answer, step_spec["answer"]):
                    raise AssertionError(f"{step_id} answer latex round-trip failed: {answer_latex}")
                answer_rows.append((step_id, step_spec["prompt"], answer_latex))
                step_obj = {
                    "id": step_id,
                    "stepAnswer": [answer_latex],
                    "problemType": "TextBox",
                    "stepTitle": step_spec["prompt"],
                    "stepBody": "Enter the value. Fractions should be in lowest terms.",
                    "answerType": "arithmetic",
                    "variabilization": {},
                    "answerLatex": answer_latex,
                }
                step_path = os.path.join(prob_dir, "steps", step_id)
                _write_json(os.path.join(step_path, f"{step_id}.json"), step_obj)
                _write_json(
                    os.path.join(step_path, "tutoring", f"{step_id}DefaultPathway.json"),
                    hint_records,
                )
                steps_out.append(step_id)
            _write_json(
                os.path.join(prob_dir, f"{prob_id}.json"),
                {
                    "id": prob_id,
                    "title": prob["title"],
                    "body": prob["body"],
                    "variabilization": {},
                    "oer": OER,
                    "license": LICENSE,
                    "lesson": lesson_spec["name"],
                    "lessonId": lesson_id,
                    "courseName": "Pre-Algebra",
                },
            )
    course = {
        "courseName": "Pre-Algebra",
        "office_hours": False,
        "language": "en",
        "courseOER": OER,
        "courseLicense": LICENSE,
        "lessons": course_lessons,
    }
    _write_json(os.path.join(OUT, "coursePlan.json"), course)
    _write_json(os.path.join(OUT, "skillModel.json"), skill_model)
    _write_json(os.path.join(OUT, "bktParams.json"), bkt)
    print(f"Wrote {len(answer_rows)} steps in {len(built_lessons)} lessons to {OUT}")
    for row in answer_rows:
        print(f"  {row[0]}  {row[2]}  {row[1][:80]}")


if __name__ == "__main__":
    emit(lessons())
