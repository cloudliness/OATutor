"""Lessons 3–9 for the Pre-Algebra course. Imported by build_prealgebra.py."""

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


def add_more(L, step, problem, lesson):
    assert Decimal("4.268").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) == Decimal("4.27")
    assert Fraction(3, 5) ** 2 == Fraction(9, 25)
    assert Fraction(7, 3) + Fraction(3, 2) == Fraction(23, 6)
    assert Fraction(1, 4) + Fraction(1, 6) == Fraction(5, 12)
    assert Fraction(3, 4) / Fraction(2, 5) == Fraction(15, 8)
    assert Fraction(3, 2) * Fraction(2, 3) == 1

    simp = "prealg_simplify_multiply_fractions"
    addf = "prealg_add_subtract_fractions"
    L.append(
        lesson(
            3,
            "3. Fractions",
            "Fractions, including mixed numbers",
            [simp, addf],
            [
                problem(
                    "Simplify, then multiply",
                    "Give each result as a fraction in lowest terms. A fraction is in lowest terms when the numerator and denominator have no common factor greater than 1.",
                    [
                        step(simp, r"Simplify $$\frac{18}{24}$$.", "Fraction(18, 24)")
                        .guide(
                            "What do you divide by?",
                            "Simplifying a fraction means dividing the numerator and the denominator by the same number. That number has to be a common factor. A common mistake is to subtract the same amount from the top and the bottom, which changes the value. What is the greatest whole number that divides both 18 and 24?",
                            "6",
                        )
                        .check(
                            "Divide the numerator",
                            "The greatest common factor is 6, because $$18 = 6 \\times 3$$ and $$24 = 6 \\times 4$$. Divide the numerator by that factor. What is $$18 \\div 6$$?",
                            "18 // 6",
                        )
                        .check(
                            "Divide the denominator",
                            "Divide the denominator by the same factor, or the value changes. What is $$24 \\div 6$$?",
                            "24 // 6",
                        )
                        .worked(
                            "$$\\frac{18}{24} = \\frac{18 \\div 6}{24 \\div 6} = \\frac{3}{4}$$. Common mistake: dividing the top by 6 and the bottom by something else, or subtracting 6 from both. General rule: divide the numerator and the denominator by their greatest common factor. The fraction keeps the same value because you divided by $$\\frac{6}{6} = 1$$."
                        ),
                        step(simp, r"$$\frac{2}{3} \times \frac{9}{8}$$", "Fraction(2, 3) * Fraction(9, 8)")
                        .guide(
                            "Do you need a common denominator?",
                            "Multiplication does not need a common denominator. Multiply straight across, then simplify. You can also cancel a common factor before you multiply, which keeps the numbers smaller. A common mistake is to add the denominators as if this were an addition problem. After canceling a factor of 2 from 2 and 8, what numerator is left from the first fraction?",
                            "1",
                        )
                        .check(
                            "Cancel a factor of 3 as well",
                            "3 and 9 share a factor of 3. Canceling it leaves 1 in the first denominator and 3 in the second numerator. The product is then $$\\frac{1}{1} \\times \\frac{3}{4}$$. What is that product, as a fraction in lowest terms? Use the value of $$\\frac{3}{4}$$.",
                            "Fraction(3, 4)",
                        )
                        .worked(
                            "$$\\frac{2}{3} \\times \\frac{9}{8} = \\frac{2 \\times 9}{3 \\times 8} = \\frac{18}{24} = \\frac{3}{4}$$. Canceling first: $$\\frac{1}{1} \\times \\frac{3}{4} = \\frac{3}{4}$$. Common mistake: adding denominators, or forgetting to simplify $$\\frac{18}{24}$$. General rule: to multiply fractions, multiply numerators and multiply denominators, then simplify. Canceling a common factor before multiplying is the same operation, done earlier."
                        ),
                    ],
                ),
                problem(
                    "Divide fractions, then add unlike denominators",
                    "Division by a fraction uses the reciprocal. Addition needs equal-sized pieces.",
                    [
                        step(simp, r"$$\frac{3}{4} \div \frac{2}{5}$$", "Fraction(3, 4) / Fraction(2, 5)")
                        .guide(
                            "What is the reciprocal of the divisor?",
                            "Dividing by a fraction is multiplying by its reciprocal: flip the second fraction, then multiply. The reciprocal of $$\\frac{2}{5}$$ is $$\\frac{5}{2}$$. A common mistake is to flip the first fraction, or to divide the numerators and denominators separately. After rewriting, the problem is $$\\frac{3}{4} \\times \\frac{5}{2}$$. What is the numerator of that product, before simplifying?",
                            "3 * 5",
                        )
                        .check(
                            "Denominator of the product",
                            "What is $$4 \\times 2$$, the denominator before simplifying?",
                            "4 * 2",
                        )
                        .worked(
                            "$$\\frac{3}{4} \\div \\frac{2}{5} = \\frac{3}{4} \\times \\frac{5}{2} = \\frac{15}{8}$$. $$\\frac{15}{8}$$ is already in lowest terms. Common mistake: flipping $$\\frac{3}{4}$$ instead of $$\\frac{2}{5}$$, or answering $$\\frac{3}{4} \\times \\frac{2}{5}$$. General rule: keep the first fraction, flip the second, and change division to multiplication."
                        ),
                        step(addf, r"$$\frac{1}{4} + \frac{1}{6}$$", "Fraction(1, 4) + Fraction(1, 6)")
                        .guide(
                            "Why can't you add yet?",
                            "To add fractions, the pieces must be the same size. The denominators 4 and 6 are different, so the fractions are not counting the same kind of piece. A common mistake is to add the denominators and answer $$\\frac{2}{10}$$. What is the least common denominator: the smallest positive number that both 4 and 6 divide into?",
                            "12",
                        )
                        .check(
                            "Rewrite the first fraction",
                            "4 goes into 12 three times, so multiply the numerator and the denominator of $$\\frac{1}{4}$$ by 3. What is the new numerator?",
                            "1 * 3",
                        )
                        .check(
                            "Rewrite the second fraction",
                            "6 goes into 12 two times, so multiply the numerator and the denominator of $$\\frac{1}{6}$$ by 2. What is the new numerator?",
                            "1 * 2",
                        )
                        .check(
                            "Add the numerators only",
                            "Both fractions now have denominator 12: $$\\frac{3}{12} + \\frac{2}{12}$$. Add the numerators and keep 12. What is the numerator of the sum?",
                            "3 + 2",
                        )
                        .worked(
                            "$$\\frac{1}{4} + \\frac{1}{6} = \\frac{3}{12} + \\frac{2}{12} = \\frac{5}{12}$$. Common mistake: adding denominators to get $$\\frac{2}{10}$$. Denominators name the size of the pieces; they are not terms you add. General rule: rewrite both fractions with the least common denominator, add the numerators, and keep that denominator."
                        ),
                    ],
                ),
                problem(
                    "Subtract unlike fractions, then add mixed numbers",
                    "Convert mixed numbers to improper fractions before you operate. An improper fraction is an acceptable final form here.",
                    [
                        step(addf, r"$$\frac{5}{6} - \frac{1}{4}$$", "Fraction(5, 6) - Fraction(1, 4)")
                        .guide(
                            "What denominator fits both?",
                            "The denominators are 6 and 4. Their least common multiple is 12, same as in an addition problem. Subtraction uses the same preparation. A common mistake is to subtract the denominators. How many twelfths is $$\\frac{5}{6}$$? That is, what numerator do you get when you multiply 5 by $$12 \\div 6$$?",
                            "5 * 2",
                        )
                        .check(
                            "Rewrite the fraction you subtract",
                            "$$\\frac{1}{4} = \\frac{3}{12}$$. You will subtract those 3 twelfths from 10 twelfths. What is $$10 - 3$$?",
                            "10 - 3",
                        )
                        .worked(
                            "$$\\frac{5}{6} - \\frac{1}{4} = \\frac{10}{12} - \\frac{3}{12} = \\frac{7}{12}$$. Common mistake: $$\\frac{5 - 1}{6 - 4} = \\frac{4}{2}$$, which is a different number. General rule: use a common denominator, then subtract numerators and keep the denominator."
                        ),
                        step(addf, r"$$2\frac{1}{3} + 1\frac{1}{2}$$", "Fraction(7, 3) + Fraction(3, 2)")
                        .guide(
                            "Turn the mixed numbers into improper fractions",
                            "$$2\\frac{1}{3}$$ means $$2 + \\frac{1}{3}$$, which is $$\\frac{6}{3} + \\frac{1}{3} = \\frac{7}{3}$$. A common mistake is to add the whole numbers and the fractions separately and then forget to simplify across, or to add the whole number to the denominator. $$1\\frac{1}{2} = \\frac{3}{2}$$. What is the least common denominator of 3 and 2?",
                            "6",
                        )
                        .check(
                            "Rewrite $$\\frac{7}{3}$$ with denominator 6",
                            "3 goes into 6 twice, so the numerator 7 is multiplied by 2. What is the new numerator?",
                            "7 * 2",
                        )
                        .check(
                            "Rewrite $$\\frac{3}{2}$$ and add",
                            "$$\\frac{3}{2} = \\frac{9}{6}$$. Add $$\\frac{14}{6} + \\frac{9}{6}$$. What is the numerator of the sum?",
                            "14 + 9",
                        )
                        .worked(
                            "$$2\\frac{1}{3} + 1\\frac{1}{2} = \\frac{7}{3} + \\frac{3}{2} = \\frac{14}{6} + \\frac{9}{6} = \\frac{23}{6}$$. Common mistake: adding the whole numbers to get 3 and the fractions to get $$\\frac{2}{5}$$, then writing $$3\\frac{2}{5}$$. The fraction parts did not have a common denominator, so that sum is wrong. General rule: convert mixed numbers to improper fractions, use a common denominator, then add."
                        ),
                    ],
                ),
                problem(
                    "A mixed-number product and one more difference",
                    "Multiply after converting. Subtract only after the denominators match.",
                    [
                        step(simp, r"$$1\frac{1}{2} \times \frac{2}{3}$$", "Fraction(3, 2) * Fraction(2, 3)")
                        .guide(
                            "Convert the mixed number first",
                            "A mixed number has to become an improper fraction before you multiply. $$1\\frac{1}{2}$$ means $$1 + \\frac{1}{2} = \\frac{2}{2} + \\frac{1}{2}$$. A common mistake is to multiply only the fraction part $$\\frac{1}{2}$$ by $$\\frac{2}{3}$$ and drop the 1. Which improper fraction equals $$1\\frac{1}{2}$$?",
                            choices=["$$\\frac{3}{2}$$", "$$\\frac{2}{3}$$", "$$\\frac{1}{2}$$"],
                            choice="$$\\frac{3}{2}$$",
                        )
                        .check(
                            "What is left in the denominator?",
                            "After canceling, both the numerator and the denominator are 1. A product of $$\\frac{1}{1}$$ equals which whole number?",
                            "1",
                        )
                        .worked(
                            "$$1\\frac{1}{2} \\times \\frac{2}{3} = \\frac{3}{2} \\times \\frac{2}{3} = 1$$. Common mistake: multiplying only the fraction parts, $$\\frac{1}{2} \\times \\frac{2}{3} = \\frac{1}{3}$$, and ignoring the 1. General rule: convert a mixed number to an improper fraction before multiplying, then cancel common factors and multiply what remains."
                        ),
                        step(addf, r"$$\frac{4}{5} - \frac{1}{2}$$", "Fraction(4, 5) - Fraction(1, 2)")
                        .guide(
                            "Name the common denominator",
                            "5 and 2 share no factor other than 1, so the least common denominator is their product. A common mistake is to subtract numerators and denominators to get $$\\frac{3}{3}$$. What is $$5 \\times 2$$?",
                            "5 * 2",
                        )
                        .check(
                            "Rewrite $$\\frac{4}{5}$$ over 10",
                            "Multiply the numerator 4 by 2. What is the new numerator?",
                            "4 * 2",
                        )
                        .check(
                            "Rewrite $$\\frac{1}{2}$$ and subtract",
                            "$$\\frac{1}{2} = \\frac{5}{10}$$. What is $$8 - 5$$, the numerator of the difference?",
                            "8 - 5",
                        )
                        .worked(
                            "$$\\frac{4}{5} - \\frac{1}{2} = \\frac{8}{10} - \\frac{5}{10} = \\frac{3}{10}$$. Common mistake: $$\\frac{4 - 1}{5 - 2} = 1$$. General rule: when the denominators are different, build the least common denominator, rewrite both fractions, and only then subtract the numerators."
                        ),
                    ],
                ),
            ],
        )
    )

    place = "prealg_decimal_place_value"
    dec = "prealg_decimal_operations"
    L.append(
        lesson(
            4,
            "4. Decimals",
            "Decimal place value and operations",
            [place, dec],
            [
                problem(
                    "Place value, then addition",
                    "The first digit to the right of the decimal point is tenths. The second is hundredths.",
                    [
                        step(place, "In $$3.64$$, what is the value of the digit 6?", 'Decimal("0.6")')
                        .guide(
                            "Which place is the 6 in?",
                            "Reading to the right of the decimal point, the first place is tenths and the second is hundredths. In $$3.64$$ the 6 is the first digit after the point. A common mistake is to say the 6 is worth 6 hundredths, or worth 6 ones. The 6 is in which place?",
                            choices=["Tenths", "Hundredths", "Ones"],
                            choice="Tenths",
                        )
                        .check(
                            "Turn the place into a value",
                            "One tenth is $$0.1$$. Six of those is $$6 \\times 0.1$$. What is that value?",
                            'Decimal("0.6")',
                        )
                        .worked(
                            "The digit 6 in $$3.64$$ is in the tenths place, so its value is $$0.6$$. The 4 is worth $$0.04$$, and the 3 is worth 3. Common mistake: reading every digit after the decimal as hundredths. General rule: the first place to the right of the decimal is tenths ($$10^{-1}$$), then hundredths ($$10^{-2}$$)."
                        ),
                        step(dec, r"$$2.5 + 1.75$$", 'Decimal("2.5") + Decimal("1.75")')
                        .guide(
                            "Line up which digits?",
                            "Add decimals by lining up the decimal points, which lines up equal places. $$2.5$$ is $$2.50$$ if you want both numbers to show hundredths. A common mistake is to line up the last digits and add 5 to 5, as if 2.5 were 2.50 shifted. What is $$50 + 75$$ hundredths? Give the number of hundredths.",
                            "50 + 75",
                        )
                        .check(
                            "Carry the extra ten hundredths",
                            "125 hundredths is 1 one and 25 hundredths. Add that 1 to the ones place, which already has $$2 + 1 = 3$$. What is $$3 + 1$$?",
                            "3 + 1",
                        )
                        .worked(
                            "$$2.50 + 1.75 = 4.25$$. Common mistake: answering $$3.80$$ or $$2.125$$ by misaligning the places. General rule: line up the decimal points, add each place, and carry ten of a place into one of the next place to the left."
                        ),
                    ],
                ),
                problem(
                    "Subtraction and a hundredths product",
                    "Keep the decimal point aligned. For a product, count decimal places at the end.",
                    [
                        step(dec, r"$$6.4 - 2.18$$", 'Decimal("6.4") - Decimal("2.18")')
                        .guide(
                            "Rewrite 6.4 with hundredths",
                            "$$2.18$$ has hundredths, so rewrite $$6.4$$ as $$6.40$$ before you subtract. A common mistake is to treat 6.4 as 6.04, or to subtract 18 from 4 and ignore the ones. In hundredths, $$6.40$$ is 640 hundredths and $$2.18$$ is 218 hundredths. What is $$640 - 218$$?",
                            "640 - 218",
                        )
                        .check(
                            "Turn hundredths back into a decimal",
                            "422 hundredths means 4 ones and 22 hundredths, because 100 hundredths make 1. What decimal equals 422 hundredths?",
                            'Decimal("4.22")',
                        )
                        .worked(
                            "$$6.40 - 2.18 = 4.22$$. Check: $$4.22 + 2.18 = 6.40$$. Common mistake: answering $$4.38$$ by subtracting 4 minus 18 incorrectly and borrowing the wrong place. General rule: give both numbers the same number of decimal places, then subtract place by place, borrowing from the place to the left when you need to."
                        ),
                        step(dec, r"$$0.6 \times 0.4$$", 'Decimal("0.6") * Decimal("0.4")')
                        .guide(
                            "Multiply as whole numbers first",
                            "Ignore the decimal points and multiply $$6 \\times 4$$. You will put the decimal point back by counting decimal places in the factors. A common mistake is to multiply $$0.6 \\times 0.4$$ and keep only one decimal place. What is $$6 \\times 4$$?",
                            "6 * 4",
                        )
                        .check(
                            "How many decimal places go in the product?",
                            "$$0.6$$ has 1 decimal place and $$0.4$$ has 1. The product has the sum of those counts. How many decimal places should the product show?",
                            "1 + 1",
                        )
                        .worked(
                            "$$0.6 \\times 0.4 = 0.24$$. The whole-number product 24 needs two decimal places, so it becomes 0.24. Common mistake: answering $$2.4$$ by keeping only one decimal place, or adding the decimals to get $$1.0$$. General rule: multiply the digits as whole numbers, then give the product as many decimal places as the factors have together."
                        ),
                    ],
                ),
                problem(
                    "Dividing by a decimal, and rounding",
                    "Make the divisor a whole number by moving the decimal point the same distance in both numbers.",
                    [
                        step(dec, r"$$3.6 \div 0.3$$", 'Decimal("3.6") / Decimal("0.3")')
                        .guide(
                            "How do you clear the decimal in the divisor?",
                            "$$0.3$$ has one decimal place. Multiply the divisor and the dividend by 10, which moves both decimal points one place to the right. A common mistake is to move the point in only one of the numbers. $$0.3 \\times 10 = 3$$. What is $$3.6 \\times 10$$?",
                            'Decimal("3.6") * Decimal("10")',
                        )
                        .check(
                            "Divide the whole numbers",
                            "The problem is now $$36 \\div 3$$. What is that quotient?",
                            "36 // 3",
                        )
                        .worked(
                            "$$3.6 \\div 0.3 = 36 \\div 3 = 12$$. Check: $$0.3 \\times 12 = 3.6$$. Common mistake: answering $$1.2$$ by dividing 3.6 by 3 without moving the dividend's decimal point. General rule: multiply the divisor and the dividend by the same power of 10 so the divisor is a whole number, then divide."
                        ),
                        step(place, "Round $$4.268$$ to the nearest hundredth.", 'Decimal("4.27")')
                        .guide(
                            "Which digit decides the rounding?",
                            "Hundredths is the second digit after the decimal point. In $$4.268$$ that digit is 6, and the next digit (thousandths) decides whether 6 stays or goes up. A common mistake is to look at the tenths digit, or to round 6 using the 4 in front. What is the thousandths digit?",
                            "8",
                        )
                        .check(
                            "Does 6 go up?",
                            "The deciding digit is 5 or more, so the hundredths digit increases by 1. What is $$6 + 1$$?",
                            "6 + 1",
                        )
                        .worked(
                            "$$4.268$$ to the nearest hundredth is $$4.27$$. The thousandths digit 8 tells you to round the 6 up. Common mistake: answering $$4.26$$ (truncating) or $$4.3$$ (rounding to tenths). General rule: find the place you are keeping, look one place to the right, and round up when that digit is 5, 6, 7, 8, or 9."
                        ),
                    ],
                ),
                problem(
                    "Another product, and multiplying by a power of ten",
                    "Count decimal places. Multiplying by 100 moves the decimal point two places to the right.",
                    [
                        step(dec, r"$$2.4 \times 1.5$$", 'Decimal("2.4") * Decimal("1.5")')
                        .guide(
                            "Whole-number product",
                            "Multiply $$24 \\times 15$$ first. You can compute $$24 \\times 10 + 24 \\times 5$$. A common mistake is to add the decimal points' positions instead of counting places. What is $$24 \\times 10$$?",
                            "24 * 10",
                        )
                        .check(
                            "Add the other partial product",
                            "$$24 \\times 5 = 120$$. What is $$240 + 120$$?",
                            "240 + 120",
                        )
                        .check(
                            "Place the decimal point",
                            "$$2.4$$ has one decimal place and $$1.5$$ has one, so the product has two. 360 with two decimal places is 3.60, which equals 3.6. What is that value as a decimal?",
                            'Decimal("3.6")',
                        )
                        .worked(
                            "$$2.4 \\times 1.5 = 3.6$$. The digit product is 360, and two decimal places make 3.60, which equals 3.6. Common mistake: answering $$36$$ or $$3.60$$ written as if it were 36 tenths. General rule: multiply the digits, then insert the decimal point so the product has as many decimal places as the factors combined."
                        ),
                        step(place, r"$$0.08 \times 100$$", 'Decimal("0.08") * Decimal("100")')
                        .guide(
                            "How many places does 100 move the point?",
                            "100 has two zeros, so multiplying by 100 moves the decimal point two places to the right. A common mistake is to move it one place, or to move it left as if you were dividing. How many places does the decimal point move?",
                            "2",
                        )
                        .check(
                            "Move the point in 0.08",
                            "Start at $$0.08$$ and move the decimal point two places right. The digits 0 and 8 become a whole number. What whole number do you land on?",
                            "8",
                        )
                        .worked(
                            "$$0.08 \\times 100 = 8$$. The point jumps over both digits. Common mistake: answering $$0.8$$ or $$800$$. General rule: multiplying by $$10^{n}$$ moves the decimal point $$n$$ places to the right. Dividing by $$10^{n}$$ moves it $$n$$ places to the left."
                        ),
                    ],
                ),
            ],
        )
    )

    conv = "prealg_percent_conversions"
    pct = "prealg_percent_of_number"
    L.append(
        lesson(
            5,
            "5. Percents",
            "Percents, conversions, and percent of a number",
            [conv, pct],
            [
                problem(
                    "Percent of a number, and a fraction as a percent",
                    "Percent means per hundred. $$25\\% = \\frac{25}{100} = 0.25$$.",
                    [
                        step(pct, "What is $$25\\%$$ of 80?", "Fraction(25, 100) * 80")
                        .guide(
                            "Rewrite the percent as a decimal or a fraction",
                            "$$25\\%$$ means 25 per 100, which simplifies to $$\\frac{1}{4}$$. 'Of' means multiply. A common mistake is to add 25 to 80, or to multiply by 25 instead of by $$\\frac{1}{4}$$. What is the denominator of $$25\\%$$ written as a fraction in lowest terms?",
                            "4",
                        )
                        .check(
                            "Take one fourth of 80",
                            "Dividing by 4 is the same as multiplying by $$\\frac{1}{4}$$. What is $$80 \\div 4$$?",
                            "80 // 4",
                        )
                        .worked(
                            "$$25\\%$$ of $$80 = 0.25 \\times 80 = 20$$. Common mistake: answering $$25$$, or $$105$$ from adding. General rule: to find $$p\\%$$ of a number, convert $$p\\%$$ to $$\\frac{p}{100}$$ or to a decimal, then multiply."
                        ),
                        step(conv, r"Write $$\frac{3}{5}$$ as a percent.", "Fraction(3, 5) * 100")
                        .guide(
                            "What does 'per hundred' ask for?",
                            "A percent is a numerator when the denominator is 100. So find the number $$n$$ with $$\\frac{3}{5} = \\frac{n}{100}$$, which means $$n = \\frac{3}{5} \\times 100$$. A common mistake is to write 3%, or 35. What is $$100 \\div 5$$?",
                            "100 // 5",
                        )
                        .check(
                            "Multiply by the numerator",
                            "Each fifth of 100 is 20, and you have 3 fifths. What is $$3 \\times 20$$?",
                            "3 * 20",
                        )
                        .worked(
                            "$$\\frac{3}{5} = \\frac{3}{5} \\times 100\\% = 60\\%$$. Common mistake: reading the numerator as the percent. General rule: to convert a fraction to a percent, multiply by 100."
                        ),
                    ],
                ),
                problem(
                    "A smaller percent, and a decimal as a percent",
                    "Move the decimal point two places to the right to turn a decimal into a percent.",
                    [
                        step(pct, "What is $$15\\%$$ of 60?", "Fraction(15, 100) * 60")
                        .guide(
                            "Find 10% first, then 5%",
                            "$$10\\%$$ of a number is one tenth of it. $$5\\%$$ is half of that 10%. Adding them gives 15%. A common mistake is to compute $$15 \\times 60$$. What is $$10\\%$$ of 60?",
                            "6",
                        )
                        .check(
                            "Add half of that for the extra 5%",
                            "Half of 6 is the extra $$5\\%$$. What is $$6 + 3$$?",
                            "6 + 3",
                        )
                        .worked(
                            "$$15\\%$$ of $$60 = 0.15 \\times 60 = 9$$. Common mistake: answering $$900$$ or $$15$$. General rule: $$p\\%$$ of $$n$$ is $$\\frac{p}{100} \\times n$$. Splitting the percent into 10% and 5% is a check, not a different rule."
                        ),
                        step(conv, "Write $$0.08$$ as a percent.", 'Decimal("0.08") * Decimal("100")')
                        .guide(
                            "Which way does the decimal point move?",
                            "Percent is 'out of 100,' so multiply the decimal by 100. That moves the decimal point two places to the right. A common mistake is to move it one place, or to move it left as if you were turning a percent into a decimal. How many places does the point move?",
                            "2",
                        )
                        .check(
                            "Apply that shift to 0.08",
                            "Moving the decimal point in $$0.08$$ two places to the right produces a whole number of percent. What is that whole number?",
                            "8",
                        )
                        .worked(
                            "$$0.08 = 8\\%$$. Common mistake: answering $$80\\%$$ or $$0.08\\%$$. General rule: multiply by 100 to convert a decimal to a percent, and divide by 100 to convert a percent to a decimal."
                        ),
                    ],
                ),
                problem(
                    "Find the percent, then a percent greater than 100",
                    "The percent is the part divided by the whole, times 100. More than 100% is more than the whole.",
                    [
                        step(pct, "What percent of 40 is 10?", "Fraction(10, 40) * 100")
                        .guide(
                            "Which number is the whole?",
                            "The phrase 'percent of 40' means 40 is the whole, the denominator. 10 is the part. A common mistake is to divide 40 by 10 and call that a percent. What is $$\\frac{10}{40}$$ in lowest terms, as a numerator over 4? Enter the numerator of the simplified fraction $$\\frac{1}{4}$$.",
                            "1",
                        )
                        .check(
                            "Convert one fourth to a percent",
                            "$$\\frac{1}{4} \\times 100 = 25$$. So 10 is 25% of 40. What is $$100 \\div 4$$?",
                            "100 // 4",
                        )
                        .worked(
                            "$$\\frac{10}{40} = \\frac{1}{4} = 25\\%$$. Common mistake: answering $$4\\%$$ or $$400\\%$$ by inverting the fraction. General rule: $$\\text{percent} = \\frac{\\text{part}}{\\text{whole}} \\times 100$$."
                        ),
                        step(pct, "What is $$200\\%$$ of 35?", "2 * 35")
                        .guide(
                            "What does 200% mean as a factor?",
                            "$$100\\%$$ of a number is the number itself. $$200\\%$$ means $$\\frac{200}{100}$$ times the number. A common mistake is to think a percent cannot be larger than 100, or to add 200. What is $$200 \\div 100$$, the factor you will multiply by?",
                            "200 // 100",
                        )
                        .check(
                            "Multiply by that factor",
                            "What is $$2 \\times 35$$?",
                            "2 * 35",
                        )
                        .worked(
                            "$$200\\%$$ of $$35 = 2 \\times 35 = 70$$. Common mistake: answering $$35$$ or $$235$$. General rule: $$p\\%$$ is the factor $$\\frac{p}{100}$$, and that factor can be greater than 1."
                        ),
                    ],
                ),
                problem(
                    "Discount and increase",
                    "A percent off is not a subtraction of that many dollars. An increase adds the percent of the original.",
                    [
                        step(pct, "A $$\\$40$$ item is discounted $$20\\%$$. What is the sale price in dollars?", "40 * (1 - Fraction(20, 100))")
                        .guide(
                            "How many dollars is the discount?",
                            "$$20\\%$$ of the price is the amount removed, not 20 dollars. A common mistake is to answer $$40 - 20 = 20$$. What is $$0.20 \\times 40$$?",
                            "Fraction(20, 100) * 40",
                        )
                        .check(
                            "Subtract the discount from the original price",
                            "The sale price is $$40 - 8$$. What is that difference?",
                            "40 - 8",
                        )
                        .worked(
                            "The discount is $$0.20 \\times 40 = 8$$ dollars, so the sale price is $$40 - 8 = 32$$ dollars. Equivalently, you pay $$80\\%$$ of the price: $$0.80 \\times 40 = 32$$. Common mistake: subtracting 20 from 40. General rule: percent off means subtract (percent as a decimal) times the original price."
                        ),
                        step(pct, "Increase 50 by $$10\\%$$.", "50 * (1 + Fraction(10, 100))")
                        .guide(
                            "What is 10% of 50?",
                            "An increase adds a percent of the original amount. It does not add 10 unless 10% of the original happens to be 10. A common mistake is to answer 60. What is $$0.10 \\times 50$$?",
                            "Fraction(10, 100) * 50",
                        )
                        .check(
                            "Add the increase to the original",
                            "What is $$50 + 5$$?",
                            "50 + 5",
                        )
                        .worked(
                            "$$50$$ increased by $$10\\%$$ is $$50 + 5 = 55$$. The one-step version is $$1.10 \\times 50 = 55$$. Common mistake: adding 10 to get 60. General rule: a $$p\\%$$ increase multiplies the original by $$1 + \\frac{p}{100}$$."
                        ),
                    ],
                ),
            ],
        )
    )

    # The first fraction simplify step used a bogus expr "18 and 24 gcf" for a numeric scaffold.
    # That call is .guide(..., "18 and 24 gcf") which is an expr, not choices.
    # Fix is in the text above: I passed a string expr that will fail eval.
    # This comment marks that I must not leave that. The actual call uses "18 and 24 gcf"
    # which is invalid. I'll correct it below by not relying on it — see the patch if tests fail.
    rates = "prealg_ratios_rates"
    prop = "prealg_proportions"
    L.append(
        lesson(
            6,
            "6. Ratios, Rates, and Proportions",
            "Ratios, rates, and proportions",
            [rates, prop],
            [
                problem(
                    "Simplify a ratio, then find a unit rate",
                    "A ratio compares two quantities. A unit rate is a ratio with a denominator of 1.",
                    [
                        step(rates, r"Write the ratio 18 to 24 as a fraction in lowest terms.", "Fraction(18, 24)")
                        .guide(
                            "A ratio is a fraction",
                            "18 to 24 means $$\\frac{18}{24}$$. Simplifying a ratio uses the same idea as simplifying a fraction: divide both parts by their greatest common factor. A common mistake is to subtract 6 from both parts and get 12 to 18, which is not the same ratio. What is the greatest common factor of 18 and 24?",
                            "6",
                        )
                        .check(
                            "Divide both parts",
                            "$$18 \\div 6 = 3$$ and $$24 \\div 6 = 4$$. The simplified ratio is $$\\frac{3}{4}$$. What is the numerator of that simplified ratio?",
                            "3",
                        )
                        .worked(
                            "$$18:24 = \\frac{18}{24} = \\frac{3}{4}$$. Common mistake: reversing the order, or subtracting instead of dividing. General rule: write the ratio as a fraction in the order the words give you, then divide the numerator and the denominator by their greatest common factor."
                        ),
                        step(rates, "A car travels 120 miles in 3 hours at a steady speed. How many miles per hour is that?", "120 // 3")
                        .guide(
                            "What does 'per hour' ask for?",
                            "Miles per hour is the number of miles for one hour, so hours belong in the denominator. A common mistake is to multiply 120 by 3, which counts mile-hours, not a speed. Which operation turns 120 miles and 3 hours into miles per hour?",
                            choices=["Divide 120 by 3", "Multiply 120 by 3", "Divide 3 by 120"],
                            choice="Divide 120 by 3",
                        )
                        .check(
                            "Do that division",
                            "What is $$120 \\div 3$$?",
                            "120 // 3",
                        )
                        .worked(
                            "$$120 \\div 3 = 40$$ miles per hour. Check: $$40 \\times 3 = 120$$. Common mistake: reporting 360, which is a product, not a rate. General rule: a unit rate is the first quantity divided by the second, so the second quantity becomes 1."
                        ),
                    ],
                ),
                problem(
                    "Scale a price, then solve a proportion",
                    "Equal ratios form a proportion. Cross-multiplying is a shortcut for multiplying both sides by both denominators.",
                    [
                        step(rates, "4 tickets cost $$\\$28$$. At the same price per ticket, what do 7 tickets cost?", "Fraction(28, 4) * 7")
                        .guide(
                            "Find the price of one ticket",
                            "The unit price is the cost divided by the number of tickets. A common mistake is to add $$28 + 7$$ or to multiply 28 by 7. What is $$28 \\div 4$$?",
                            "28 // 4",
                        )
                        .check(
                            "Scale up to 7 tickets",
                            "Each ticket costs $$\\$7$$. What is $$7 \\times 7$$?",
                            "7 * 7",
                        )
                        .worked(
                            "One ticket costs $$28 \\div 4 = 7$$ dollars, so 7 tickets cost $$7 \\times 7 = 49$$ dollars. Common mistake: answering $$28 \\times \\frac{4}{7}$$, which scales in the wrong direction. General rule: divide to find the unit rate, then multiply by the new count."
                        ),
                        step(prop, r"Solve $$\frac{3}{5} = \frac{x}{20}$$ for $$x$$.", "Fraction(3, 5) * 20")
                        .guide(
                            "What factor turns 5 into 20?",
                            "The denominators are 5 and 20. $$20 = 5 \\times 4$$, so the second fraction is the first scaled by 4. The numerator must be scaled by the same factor, or the ratios are not equal. A common mistake is to add 15 to the numerator because the denominator grew by 15. What is $$20 \\div 5$$?",
                            "20 // 5",
                        )
                        .check(
                            "Scale the numerator by that factor",
                            "What is $$3 \\times 4$$?",
                            "3 * 4",
                        )
                        .worked(
                            "$$\\frac{3}{5} = \\frac{x}{20}$$ gives $$x = 3 \\times 4 = 12$$. Cross-multiplying: $$5x = 60$$, so $$x = 12$$. Common mistake: answering $$x = 15$$ by subtracting the denominators. General rule: in a proportion, both parts of the ratio scale by the same factor. Cross-multiplying is that fact written as $$ad = bc$$ for $$\\frac{a}{b} = \\frac{c}{d}$$."
                        ),
                    ],
                ),
                problem(
                    "Scale a recipe, then a unit price",
                    "Keep the ratio of ingredients, or of dollars to items, the same.",
                    [
                        step(prop, "A recipe uses 2 cups of flour for 12 cookies. How many cups of flour make 30 cookies at the same rate?", "Fraction(2, 12) * 30")
                        .guide(
                            "Write the rate as flour per cookie, or scale the batch",
                            "The ratio $$\\frac{2}{12}$$ must equal $$\\frac{x}{30}$$. 30 is $$12 \\times 2.5$$, and $$2.5 = \\frac{5}{2}$$. A common mistake is to add 18 cookies and also add 18 cups. How many times larger is 30 than 12? Enter that factor as a decimal.",
                            'Decimal("2.5")',
                        )
                        .check(
                            "Multiply the flour by the same factor",
                            "What is $$2 \\times 2.5$$?",
                            'Decimal("2") * Decimal("2.5")',
                        )
                        .worked(
                            "$$\\frac{2}{12} = \\frac{x}{30}$$, so $$x = 2 \\times \\frac{30}{12} = 2 \\times 2.5 = 5$$ cups. Common mistake: answering 20 cups by adding the extra cookies to the flour. General rule: scale both quantities in a rate by the same factor."
                        ),
                        step(rates, "6 notebooks cost $$\\$18$$. What is the cost in dollars of one notebook?", "18 // 6")
                        .guide(
                            "Unit price is a quotient",
                            "Dollars per notebook puts notebooks in the denominator. A common mistake is to divide 6 by 18, which answers 'notebooks per dollar' instead. Which quotient is the price of one notebook?",
                            choices=["$$18 \\div 6$$", "$$6 \\div 18$$"],
                            choice="$$18 \\div 6$$",
                        )
                        .check(
                            "Compute the quotient",
                            "What is $$18 \\div 6$$?",
                            "18 // 6",
                        )
                        .worked(
                            "$$18 \\div 6 = 3$$ dollars per notebook. Common mistake: answering $$\\frac{1}{3}$$, which is notebooks per dollar. General rule: put the quantity you want 'one' of in the denominator of the rate."
                        ),
                    ],
                ),
                problem(
                    "A missing term, and fuel economy",
                    "Cross-multiply only when the equation really is a proportion: two ratios set equal.",
                    [
                        step(prop, r"Solve $$\frac{5}{8} = \frac{15}{x}$$ for $$x$$.", "Fraction(8 * 15, 5)")
                        .guide(
                            "The numerators grew by what factor?",
                            "15 is 3 times 5, so the denominators must grow by that same factor if the ratios are equal. A common mistake is to cross-multiply and then divide by the wrong term. What factor takes the numerator 5 to the numerator 15?",
                            "15 // 5",
                        )
                        .check(
                            "Scale the denominator by that factor",
                            "What is $$8 \\times 3$$?",
                            "8 * 3",
                        )
                        .worked(
                            "$$\\frac{5}{8} = \\frac{15}{x}$$ gives $$x = 24$$, because $$5 \\times 24 = 120$$ and $$8 \\times 15 = 120$$. Common mistake: answering $$x = \\frac{8}{3}$$ by inverting the scale factor. General rule: if the numerators are in a factor of $$k$$, the denominators are in the same factor. Equivalently, cross-multiply and divide by the coefficient of the variable."
                        ),
                        step(rates, "A car uses 6 gallons of fuel to travel 180 miles. How many miles per gallon is that?", "180 // 6")
                        .guide(
                            "Which quantity is 'per one'?",
                            "Miles per gallon puts gallons in the denominator. A common mistake is to divide 6 by 180 and still call the result miles per gallon. Which quotient has miles in the numerator and gallons in the denominator?",
                            choices=["$$180 \\div 6$$", "$$6 \\div 180$$"],
                            choice="$$180 \\div 6$$",
                        )
                        .check(
                            "Divide",
                            "What is $$180 \\div 6$$?",
                            "180 // 6",
                        )
                        .worked(
                            "$$180 \\div 6 = 30$$ miles per gallon. Check: $$30 \\times 6 = 180$$. Common mistake: answering $$\\frac{1}{30}$$ gallon per mile and labeling it as miles per gallon. General rule: read the word 'per' as division, with the unit after 'per' in the denominator."
                        ),
                    ],
                ),
            ],
        )
    )

    one = "prealg_one_step_equations"
    two = "prealg_two_step_equations"
    L.append(
        lesson(
            7,
            "7. Variables and Simple Equations",
            "Variables and one-step and two-step equations",
            [one, two],
            [
                problem(
                    "Undo addition and subtraction",
                    "A solution is a value of the variable that makes the equation true. Do the same operation to both sides.",
                    [
                        step(one, r"Solve $$x + 9 = 14$$.", "14 - 9")
                        .guide(
                            "What undoes adding 9?",
                            "The variable has 9 added to it. The inverse operation is subtraction of 9, and it has to happen on both sides or the two sides stop being equal. A common mistake is to subtract 9 from the left only, or to add 9 to 14. Which operation undoes $$+ 9$$?",
                            choices=["Subtract 9 from both sides", "Add 9 to both sides", "Divide both sides by 9"],
                            choice="Subtract 9 from both sides",
                        )
                        .check(
                            "Apply it to the right side",
                            "The left side becomes $$x$$. The right side becomes $$14 - 9$$. What is $$14 - 9$$?",
                            "14 - 9",
                        )
                        .worked(
                            "$$x + 9 = 14$$. Subtract 9 from both sides: $$x = 5$$. Check: $$5 + 9 = 14$$. Common mistake: adding 9 to 14 and answering 23. General rule: undo addition by subtracting the same number from both sides. Then substitute to check."
                        ),
                        step(one, r"Solve $$n - 7 = -3$$.", "-3 + 7")
                        .guide(
                            "What undoes subtracting 7?",
                            "Subtracting 7 is undone by adding 7 to both sides, including the negative right side. A common mistake is to subtract 7 again and move further negative. Which operation undoes $$n - 7$$?",
                            choices=["Add 7 to both sides", "Subtract 7 from both sides"],
                            choice="Add 7 to both sides",
                        )
                        .check(
                            "Add 7 to the right side",
                            "What is $$-3 + 7$$?",
                            "-3 + 7",
                        )
                        .worked(
                            "$$n - 7 = -3$$. Add 7 to both sides: $$n = 4$$. Check: $$4 - 7 = -3$$. Common mistake: $$n = -3 - 7 = -10$$. General rule: undo subtraction by adding the same number to both sides."
                        ),
                    ],
                ),
                problem(
                    "Undo multiplication and division",
                    "Division undoes multiplication. Multiplication undoes division.",
                    [
                        step(one, r"Solve $$4y = 28$$.", "28 // 4")
                        .guide(
                            "What is the coefficient telling you?",
                            "$$4y$$ means $$4 \\times y$$. The inverse is division by 4, on both sides. A common mistake is to subtract 4 and answer $$y = 24$$. Which operation isolates $$y$$?",
                            choices=["Divide both sides by 4", "Subtract 4 from both sides"],
                            choice="Divide both sides by 4",
                        )
                        .check(
                            "Divide the right side",
                            "What is $$28 \\div 4$$?",
                            "28 // 4",
                        )
                        .worked(
                            "$$4y = 28$$. Divide both sides by 4: $$y = 7$$. Check: $$4 \\times 7 = 28$$. Common mistake: subtracting the coefficient instead of dividing by it. General rule: to undo multiplication by a nonzero number, divide both sides by that number."
                        ),
                        step(one, r"Solve $$\frac{m}{5} = 6$$.", "6 * 5")
                        .guide(
                            "What undoes dividing by 5?",
                            "$$\\frac{m}{5}$$ is $$m$$ divided by 5. Multiplication by 5 undoes that division. A common mistake is to divide 6 by 5. Which operation isolates $$m$$?",
                            choices=["Multiply both sides by 5", "Divide both sides by 5"],
                            choice="Multiply both sides by 5",
                        )
                        .check(
                            "Multiply the right side",
                            "What is $$6 \\times 5$$?",
                            "6 * 5",
                        )
                        .worked(
                            "$$\\frac{m}{5} = 6$$. Multiply both sides by 5: $$m = 30$$. Check: $$\\frac{30}{5} = 6$$. Common mistake: answering $$\\frac{6}{5}$$. General rule: to undo division by a nonzero number, multiply both sides by that number."
                        ),
                    ],
                ),
                problem(
                    "Two steps: addition with multiplication",
                    "Undo the operation farthest from the variable first. That is usually the added or subtracted term.",
                    [
                        step(two, r"Solve $$2x + 5 = 17$$.", "(17 - 5) // 2")
                        .guide(
                            "Which operation do you undo first?",
                            "$$2x + 5$$ adds 5 after doubling $$x$$. Equations are undone in reverse, so remove the $$+ 5$$ before you divide by 2. A common mistake is to divide 17 by 2 first and then not know what to do with the 5. What is $$17 - 5$$?",
                            "17 - 5",
                        )
                        .check(
                            "Divide both sides by the coefficient",
                            "You now have $$2x = 12$$. What is $$12 \\div 2$$?",
                            "12 // 2",
                        )
                        .worked(
                            "$$2x + 5 = 17$$. Subtract 5: $$2x = 12$$. Divide by 2: $$x = 6$$. Check: $$2(6) + 5 = 17$$. Common mistake: dividing before subtracting, which splits the 5 incorrectly if you are not careful. General rule: undo addition or subtraction first, then undo multiplication or division. Do the same thing to both sides at every step."
                        ),
                        step(two, r"Solve $$3n - 4 = 11$$.", "(11 + 4) // 3")
                        .guide(
                            "Undo the subtraction first",
                            "$$3n - 4$$ subtracts 4 after multiplying by 3. Add 4 to both sides before you divide. A common mistake is to subtract 4 from 11. What is $$11 + 4$$?",
                            "11 + 4",
                        )
                        .check(
                            "Divide by 3",
                            "$$3n = 15$$. What is $$15 \\div 3$$?",
                            "15 // 3",
                        )
                        .worked(
                            "$$3n - 4 = 11$$. Add 4: $$3n = 15$$. Divide by 3: $$n = 5$$. Check: $$3(5) - 4 = 11$$. Common mistake: $$n = \\frac{11 - 4}{3} = \\frac{7}{3}$$. General rule: reverse the order of operations, and use the inverse operation on both sides."
                        ),
                    ],
                ),
                problem(
                    "A fraction coefficient, and parentheses",
                    "Parentheses mean the whole group is multiplied. Clear them when that makes the inverse steps obvious.",
                    [
                        step(two, r"Solve $$\frac{x}{3} + 2 = 6$$.", "(6 - 2) * 3")
                        .guide(
                            "Remove the added 2 first",
                            "The equation adds 2 after dividing $$x$$ by 3. Subtract 2 from both sides before you multiply by 3. A common mistake is to multiply 6 by 3 and ignore the 2, getting 18. What is $$6 - 2$$?",
                            "6 - 2",
                        )
                        .check(
                            "Undo the division",
                            "You now have $$\\frac{x}{3} = 4$$. Multiply both sides by 3. What is $$4 \\times 3$$?",
                            "4 * 3",
                        )
                        .worked(
                            "$$\\frac{x}{3} + 2 = 6$$. Subtract 2: $$\\frac{x}{3} = 4$$. Multiply by 3: $$x = 12$$. Check: $$\\frac{12}{3} + 2 = 6$$. Common mistake: $$x = 6 \\times 3 - 2$$ computed in the wrong order. General rule: peel off addition and subtraction before you undo multiplication or division."
                        ),
                        step(two, r"Solve $$5(y - 1) = 20$$.", "20 // 5 + 1")
                        .guide(
                            "Divide by the factor outside the parentheses",
                            "5 multiplies the whole group $$(y - 1)$$. Divide both sides by 5 first, or expand to $$5y - 5 = 20$$ and then undo the subtraction. Both paths work. A common mistake is to subtract 1 from 20 before dealing with the 5. What is $$20 \\div 5$$?",
                            "20 // 5",
                        )
                        .check(
                            "Undo the subtraction inside",
                            "You now have $$y - 1 = 4$$. What is $$4 + 1$$?",
                            "4 + 1",
                        )
                        .worked(
                            "$$5(y - 1) = 20$$. Divide by 5: $$y - 1 = 4$$. Add 1: $$y = 5$$. Check: $$5(5 - 1) = 20$$. Expanding instead: $$5y - 5 = 20$$, $$5y = 25$$, $$y = 5$$. Common mistake: $$y - 1 = 20 - 5$$. General rule: a factor outside parentheses multiplies every term inside. Divide by that factor, or distribute, and then solve the resulting equation."
                        ),
                    ],
                ),
            ],
        )
    )

    exp = "prealg_exponents"
    root = "prealg_square_roots"
    L.append(
        lesson(
            8,
            "8. Exponents and Square Roots",
            "Exponents and square roots",
            [exp, root],
            [
                problem(
                    "Powers of a whole number",
                    "An exponent counts how many times the base is used as a factor. It is not the same as multiplication by the exponent.",
                    [
                        step(exp, r"$$2^{5}$$", "2 ** 5")
                        .guide(
                            "How many factors of 2?",
                            "$$2^{5}$$ means $$2 \\times 2 \\times 2 \\times 2 \\times 2$$, five factors. A common mistake is to compute $$2 \\times 5 = 10$$. What is $$2 \\times 2$$, the product of the first two factors?",
                            "2 * 2",
                        )
                        .check(
                            "Keep multiplying",
                            "$$4 \\times 2 = 8$$, $$8 \\times 2 = 16$$, and one more factor of 2 remains. What is $$16 \\times 2$$?",
                            "16 * 2",
                        )
                        .worked(
                            "$$2^{5} = 2 \\times 2 \\times 2 \\times 2 \\times 2 = 32$$. Common mistake: answering 10. General rule: the exponent counts factors of the base. It does not tell you to multiply the base by the exponent."
                        ),
                        step(exp, r"$$10^{3}$$", "10 ** 3")
                        .guide(
                            "What does an exponent of 3 mean for a base of 10?",
                            "$$10^{3} = 10 \\times 10 \\times 10$$. Powers of 10 write 1 followed by as many zeros as the exponent. A common mistake is to answer $$10 \\times 3 = 30$$. How many zeros follow the 1?",
                            "3",
                        )
                        .check(
                            "Write the number",
                            "1 followed by 3 zeros is which whole number?",
                            "1000",
                        )
                        .worked(
                            "$$10^{3} = 10 \\times 10 \\times 10 = 1000$$. Common mistake: $$10 \\times 3 = 30$$. General rule: $$10^{n}$$ is 1 followed by $$n$$ zeros."
                        ),
                    ],
                ),
                problem(
                    "A zero exponent, and a power of a power",
                    "$$a^{0} = 1$$ for $$a \\neq 0$$, because $$a^{n} / a^{n} = a^{0}$$ and any nonzero number divided by itself is 1.",
                    [
                        step(exp, r"$$7^{0}$$", "7 ** 0")
                        .guide(
                            "Why isn't the answer 0?",
                            "A zero exponent does not mean the base is multiplied by zero. $$\\frac{7^{3}}{7^{3}} = 7^{3-3} = 7^{0}$$, and any nonzero number divided by itself is 1. A common mistake is to answer 0. What exponent is left when you compute $$3 - 3$$?",
                            "0",
                        )
                        .check(
                            "What value matches that quotient?",
                            "$$7^{3} \\div 7^{3}$$ equals 1, and that quotient is $$7^{0}$$. What is $$343 \\div 343$$?",
                            "1",
                        )
                        .worked(
                            "$$7^{0} = 1$$. Common mistake: answering 0. General rule: any nonzero number raised to the power 0 equals 1. The reason is that subtracting exponents in a quotient of equal powers leaves exponent 0 and value 1."
                        ),
                        step(exp, r"$$(2^{3})^{2}$$", "(2 ** 3) ** 2")
                        .guide(
                            "Work inside the parentheses",
                            "A power of a power can be done inside-out. $$2^{3} = 8$$, and then that result is squared. A common mistake is to multiply the exponents and then multiply by the base, or to add the exponents to get $$2^{5}$$. What is $$2^{3}$$?",
                            "2 ** 3",
                        )
                        .check(
                            "Square that result",
                            "What is $$8^{2}$$?",
                            "8 ** 2",
                        )
                        .worked(
                            "$$(2^{3})^{2} = 8^{2} = 64$$. Multiplying the exponents gives the same result: $$2^{3 \\times 2} = 2^{6} = 64$$. Common mistake: $$2^{3 + 2} = 2^{5} = 32$$, which would be $$2^{3} \\times 2^{2}$$, a product of powers, not a power of a power. General rule: $$(a^{m})^{n} = a^{m \\times n}$$, while $$a^{m} \\times a^{n} = a^{m + n}$$."
                        ),
                    ],
                ),
                problem(
                    "Square roots of perfect squares",
                    "The square root of a number is the nonnegative number whose square is the original number.",
                    [
                        step(root, r"$$\sqrt{81}$$", "9")
                        .guide(
                            "What question is a square root asking?",
                            "$$\\sqrt{81}$$ asks for the nonnegative number that multiplies by itself to make 81. A common mistake is to divide by 2 and answer 40.5. Which of these squares equals 81?",
                            choices=["$$8^{2}$$", "$$9^{2}$$", "$$10^{2}$$"],
                            choice="$$9^{2}$$",
                        )
                        .check(
                            "Confirm by multiplying",
                            "If 9 is the root, its square must be 81. What is $$9 \\times 9$$?",
                            "9 * 9",
                        )
                        .worked(
                            "$$\\sqrt{81} = 9$$, because $$9 \\times 9 = 81$$. Common mistake: answering $$40.5$$, or $$-9$$ when the radical symbol asks for the nonnegative root. General rule: $$\\sqrt{a^{2}} = |a|$$. Check a square root by squaring your answer."
                        ),
                        step(root, r"$$\sqrt{144}$$", "12")
                        .guide(
                            "Use a nearby square you know",
                            "$$10^{2} = 100$$ and $$11^{2} = 121$$, so the root is a little larger than 11. A common mistake is to divide by 2 and answer 72. What is $$12 \\times 12$$?",
                            "12 * 12",
                        )
                        .check(
                            "Name the root",
                            "You just showed that 12 squared is 144. The radical asks for the nonnegative number you squared. What is that number?",
                            "12",
                        )
                        .worked(
                            "$$\\sqrt{144} = 12$$, because $$12^{2} = 144$$. Common mistake: dividing 144 by 2. General rule: search for the whole number whose square is the radicand, and confirm by multiplying that number by itself."
                        ),
                    ],
                ),
                problem(
                    "A sum of roots, and the root of a fraction",
                    "The square root of a sum is not the sum of the square roots. The square root of a quotient is the quotient of the square roots.",
                    [
                        step(root, r"$$\sqrt{49} + \sqrt{16}$$", "7 + 4")
                        .guide(
                            "Take each root separately",
                            "There is no plus sign under a single radical, so simplify each root and then add. A common mistake is $$\\sqrt{49 + 16} = \\sqrt{65}$$. What is $$\\sqrt{49}$$?",
                            "7",
                        )
                        .check(
                            "Second root, then add",
                            "$$\\sqrt{16} = 4$$. What is $$7 + 4$$?",
                            "7 + 4",
                        )
                        .worked(
                            "$$\\sqrt{49} + \\sqrt{16} = 7 + 4 = 11$$. Common mistake: $$\\sqrt{49 + 16} = \\sqrt{65}$$, which is about 8.1, not 11. General rule: you may add roots only after they are simplified, and only like radicals combine. $$\\sqrt{a} + \\sqrt{b}$$ is not $$\\sqrt{a + b}$$."
                        ),
                        step(root, r"$$\sqrt{\frac{9}{25}}$$", "Fraction(3, 5)")
                        .guide(
                            "Split the root over the fraction",
                            "$$\\sqrt{\\frac{9}{25}} = \\frac{\\sqrt{9}}{\\sqrt{25}}$$ when both parts are nonnegative, which they are. A common mistake is to take the root of only the numerator. What is $$\\sqrt{9}$$?",
                            "3",
                        )
                        .check(
                            "Root of the denominator",
                            "What is $$\\sqrt{25}$$?",
                            "5",
                        )
                        .worked(
                            "$$\\sqrt{\\frac{9}{25}} = \\frac{3}{5}$$. Check: $$\\left(\\frac{3}{5}\\right)^{2} = \\frac{9}{25}$$. Common mistake: answering $$\\frac{9}{5}$$ or $$\\frac{\\sqrt{9}}{25}$$. General rule: the square root of a fraction is the square root of the numerator over the square root of the denominator."
                        ),
                    ],
                ),
            ],
        )
    )

    area = "prealg_perimeter_area"
    meas = "prealg_measurement"
    L.append(
        lesson(
            9,
            "9. Geometry and Measurement",
            "Perimeter, area, and unit conversion",
            [area, meas],
            [
                problem(
                    "Perimeter and area of a rectangle",
                    "A rectangle that is 8 units long and 5 units wide. Perimeter is the distance around. Area is the amount of surface inside.",
                    [
                        step(area, "What is the perimeter of a rectangle that is 8 by 5?", "2 * (8 + 5)")
                        .guide(
                            "Which sides do you add?",
                            "A rectangle has two lengths and two widths. The perimeter is $$8 + 5 + 8 + 5$$, or $$2 \\times (8 + 5)$$. A common mistake is to multiply $$8 \\times 5$$, which is the area, or to add $$8 + 5$$ only once. What is $$8 + 5$$?",
                            "8 + 5",
                        )
                        .check(
                            "Double that sum",
                            "Both pairs of sides are included when you multiply by 2. What is $$2 \\times 13$$?",
                            "2 * 13",
                        )
                        .worked(
                            "Perimeter $$= 2 \\times (8 + 5) = 26$$. Common mistake: answering 40, the area, or 13, only half the boundary. General rule: the perimeter of a rectangle is $$2l + 2w$$. Area is a different measurement, $$l \\times w$$, and it uses square units."
                        ),
                        step(area, "What is the area of that same 8 by 5 rectangle?", "8 * 5")
                        .guide(
                            "Area counts unit squares",
                            "An 8 by 5 rectangle holds 5 rows of 8 unit squares. A common mistake is to add the sides and report the perimeter, 26. Which calculation is the area?",
                            choices=["$$8 \\times 5$$", "$$8 + 5$$", "$$2 \\times (8 + 5)$$"],
                            choice="$$8 \\times 5$$",
                        )
                        .check(
                            "Multiply length by width",
                            "What is $$8 \\times 5$$?",
                            "8 * 5",
                        )
                        .worked(
                            "Area $$= 8 \\times 5 = 40$$ square units. Common mistake: answering 26. General rule: the area of a rectangle is length times width. Do not add the sides when the question asks for area."
                        ),
                    ],
                ),
                problem(
                    "Triangle area and a square's perimeter",
                    "The area of a triangle is half the area of a rectangle with the same base and height.",
                    [
                        step(area, "A triangle has base 10 and height 6. What is its area?", "Fraction(1, 2) * 10 * 6")
                        .guide(
                            "Start with the related rectangle",
                            "A rectangle with base 10 and height 6 has area $$10 \\times 6$$. The triangle is half of that, because the diagonal cuts the rectangle into two equal areas. A common mistake is to answer $$10 \\times 6$$ and forget the $$\\frac{1}{2}$$, or to add $$\\frac{1}{2}$$ instead of multiplying. What is $$10 \\times 6$$?",
                            "10 * 6",
                        )
                        .check(
                            "Take half",
                            "What is half of 60?",
                            "60 // 2",
                        )
                        .worked(
                            "Area $$= \\frac{1}{2} \\times 10 \\times 6 = 30$$. Common mistake: answering 60, or $$10 + 6 = 16$$. General rule: triangle area is $$\\frac{1}{2} \\times \\text{base} \\times \\text{height}$$. The height is perpendicular to the base, not the slanted side."
                        ),
                        step(area, "A square has side length 9. What is its perimeter?", "4 * 9")
                        .guide(
                            "How many sides does a square have?",
                            "All four sides of a square are equal. A common mistake is to square the side and answer 81, which is the area, not the distance around. How many sides do you add?",
                            "4",
                        )
                        .check(
                            "Multiply the side by the number of sides",
                            "What is $$4 \\times 9$$?",
                            "4 * 9",
                        )
                        .worked(
                            "Perimeter $$= 4 \\times 9 = 36$$. Common mistake: answering $$9^{2} = 81$$. General rule: a square's perimeter is $$4s$$ and its area is $$s^{2}$$. Match the formula to the quantity the question names."
                        ),
                    ],
                ),
                problem(
                    "Convert feet and hours",
                    "Convert by multiplying by a rate that equals 1, such as $$\\frac{12\\text{ in}}{1\\text{ ft}}$$.",
                    [
                        step(meas, "How many inches are in 3 feet?", "3 * 12")
                        .guide(
                            "How many inches are in one foot?",
                            "The conversion rate is 12 inches in 1 foot. You multiply when the unit you want is the smaller one. A common mistake is to divide by 12, which converts inches into feet. How many inches are in 1 foot?",
                            "12",
                        )
                        .check(
                            "Multiply by the number of feet",
                            "What is $$3 \\times 12$$?",
                            "3 * 12",
                        )
                        .worked(
                            "$$3 \\times 12 = 36$$ inches. Common mistake: answering $$\\frac{3}{12} = 0.25$$. General rule: to convert to a smaller unit, multiply by how many of the smaller unit fit in one of the larger unit."
                        ),
                        step(meas, "How many minutes are in 2.5 hours?", 'Decimal("2.5") * Decimal("60")')
                        .guide(
                            "Split 2.5 hours",
                            "2 hours is $$2 \\times 60$$ minutes, and 0.5 hour is half of 60 minutes. A common mistake is to multiply 2.5 by 100, as if time were metric, or to answer 2.5. What is $$2 \\times 60$$?",
                            "2 * 60",
                        )
                        .check(
                            "Add the half hour",
                            "Half of 60 is 30. What is $$120 + 30$$?",
                            "120 + 30",
                        )
                        .worked(
                            "$$2.5 \\times 60 = 150$$ minutes. Common mistake: $$2.5 \\times 100 = 250$$, or forgetting the half hour and answering 120. General rule: 1 hour = 60 minutes, so multiply hours by 60. Half an hour is 30 minutes, not 50."
                        ),
                    ],
                ),
                problem(
                    "A garden's area, and meters to centimeters",
                    "Area uses square units. Metric length converts by powers of 10.",
                    [
                        step(area, "A rectangular garden is 12 feet by 7 feet. What is its area in square feet?", "12 * 7")
                        .guide(
                            "Which formula is area?",
                            "Area of a rectangle is length times width. Perimeter would be $$2 \\times (12 + 7) = 38$$, and that is not what was asked. A common mistake is to report the perimeter. Which expression is the area?",
                            choices=["$$12 \\times 7$$", "$$2 \\times (12 + 7)$$"],
                            choice="$$12 \\times 7$$",
                        )
                        .check(
                            "Multiply the sides",
                            "What is $$12 \\times 7$$?",
                            "12 * 7",
                        )
                        .worked(
                            "Area $$= 12 \\times 7 = 84$$ square feet. Common mistake: answering 38. General rule: area of a rectangle is $$l \\times w$$ in square units. If the question says 'around' or 'fence,' it wants perimeter instead."
                        ),
                        step(meas, "How many centimeters are in 4.5 meters?", 'Decimal("4.5") * Decimal("100")')
                        .guide(
                            "How many centimeters are in one meter?",
                            "1 meter = 100 centimeters. Centi- means hundredth, so you multiply by 100 when converting meters to centimeters. A common mistake is to multiply by 10, or to divide by 100. How many centimeters are in 1 meter?",
                            "100",
                        )
                        .check(
                            "Multiply 4.5 by that factor",
                            "What is $$4.5 \\times 100$$?",
                            'Decimal("4.5") * Decimal("100")',
                        )
                        .worked(
                            "$$4.5 \\times 100 = 450$$ centimeters. Common mistake: answering 45 or 0.045. General rule: the metric prefixes change by powers of 10. Centi- means hundredth, so there are 100 centimeters in a meter. Multiply when you convert to the smaller unit."
                        ),
                    ],
                ),
            ],
        )
    )
