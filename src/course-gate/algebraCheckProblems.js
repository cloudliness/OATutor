/**
 * One problem from each major Elementary Algebra topic.
 * All are single-step arithmetic items already in the OATutor pool,
 * chosen because the official answer checks out and no figure is required.
 * 16 of 20 is exactly 80%.
 */
export const ALGEBRA_CHECK_PROBLEMS = [
    {
        id: "a4d2b33use34",
        topic: "Order of operations",
        review: "Parentheses first, then multiplication and division from left to right, then addition and subtraction. Do not add two numbers just because they are written next to each other.",
    },
    {
        id: "a9ae528add6",
        topic: "Integers and absolute value",
        review: "Work inside absolute-value bars before you remove them. Absolute value is a distance, so it is never negative.",
    },
    {
        id: "aafc2dcMultiply23",
        topic: "Integer exponents and division",
        review: "An exponent applies before division. A negative base in parentheses, raised to an even power, is positive.",
    },
    {
        id: "ab3c11fVisualize6",
        topic: "Multiplying fractions",
        review: "Multiply numerators and multiply denominators. A leading minus makes the product negative. Simplify at the end.",
    },
    {
        id: "ac9c764addand5",
        topic: "Adding fractions",
        review: "Fractions need a common denominator before you add. Add numerators and keep the denominator. Do not add denominators.",
    },
    {
        id: "ad4e7e2decimals14",
        topic: "Adding decimals",
        review: "Line up the decimal points so tenths add to tenths and hundredths add to hundredths.",
    },
    {
        id: "a453be6realnumbers10",
        topic: "Square roots",
        review: "The square root is the nonnegative number that squares to the radicand. Check by multiplying your answer by itself.",
    },
    {
        id: "a9c142dVarCon9",
        topic: "Variables on both sides",
        review: "Collect the variable terms on one side by adding or subtracting the same amount on both sides, then isolate the variable.",
    },
    {
        id: "ab1ad7fGenStr12",
        topic: "Multi-step linear equations",
        review: "Clear parentheses first, then undo addition and subtraction, then undo multiplication. Do the same operation to both sides.",
    },
    {
        id: "a8583b4FracDec6",
        topic: "Equations with fraction coefficients",
        review: "Combine the fraction coefficients over a common denominator, then multiply both sides by that denominator.",
    },
    {
        id: "a3e5c4cpercent2",
        topic: "Percent of a number",
        review: "Percent means per hundred. Convert the percent to a decimal or a fraction, then multiply.",
    },
    {
        id: "a870b02DivMul19",
        topic: "Solving a linear equation",
        review: "Simplify each side first. Then divide both sides by the coefficient of the variable.",
    },
    {
        id: "a012999exa2",
        topic: "The distributive property",
        review: "A factor outside parentheses multiplies every term inside. Multiply, then add the resulting terms.",
    },
    {
        id: "a1279cdpowers8",
        topic: "Power of a product",
        review: "A power outside parentheses applies to every factor inside, including the sign. Multiply the exponents.",
    },
    {
        id: "a0ca101exe13",
        topic: "Factoring trinomials",
        review: "For x² + bx + c, look for two numbers that multiply to c and add to b. Check by multiplying your factors back together.",
    },
    {
        id: "a104861trifactor26",
        topic: "Factoring special products",
        review: "Look for a greatest common factor first. A perfect-square trinomial factors as a squared binomial.",
    },
    {
        id: "a171b3arationals27",
        topic: "Simplifying rational numbers",
        review: "Divide the numerator and the denominator by their greatest common factor. Keep the sign with the numerator or out in front.",
    },
    {
        id: "ab62b81rational9",
        topic: "Adding rational expressions",
        review: "When the denominators already match, add the numerators and keep that denominator.",
    },
    {
        id: "aaff50dradical25",
        topic: "Simplifying square roots",
        review: "Factor out the largest perfect square. The square root of a product is the product of the square roots.",
    },
    {
        id: "a5c70bfsquareroots18",
        topic: "Adding like square roots",
        review: "Like radicals add the way like terms do. Add the coefficients and keep the radical. Unlike radicals do not combine.",
    },
];

export const ALGEBRA_CHECK_PASS_COUNT = Math.ceil(
    ALGEBRA_CHECK_PROBLEMS.length * 0.8
);
