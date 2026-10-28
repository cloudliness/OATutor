/**
 * Course unlock for a personal study copy.
 * Pre-Algebra and OpenStax Elementary Algebra are available immediately.
 * Every other course stays locked until the Algebra Check is passed at 80%,
 * or until every Elementary Algebra lesson is mastered. The flag lives in
 * localStorage on this browser.
 */

export const UNLOCK_STORAGE_KEY = "oatutor-advanced-unlock";
export const PASS_RATIO = 0.8;
export const PREALGEBRA_COURSE = "Pre-Algebra";
export const ELEMENTARY_ALGEBRA_COURSE = "OpenStax: Elementary Algebra";

const FOUNDATIONAL = new Set([PREALGEBRA_COURSE, ELEMENTARY_ALGEBRA_COURSE]);

export function isFoundationalCourse(courseName) {
    return FOUNDATIONAL.has(courseName);
}

export function readUnlockRecord() {
    if (typeof window === "undefined") return null;
    try {
        const raw = window.localStorage.getItem(UNLOCK_STORAGE_KEY);
        if (!raw) return null;
        const parsed = JSON.parse(raw);
        if (!parsed || parsed.unlocked !== true) return null;
        return parsed;
    } catch (err) {
        return null;
    }
}

export function isAdvancedUnlocked() {
    return readUnlockRecord() != null;
}

export function isCourseUnlocked(courseName) {
    if (!courseName || isFoundationalCourse(courseName)) return true;
    return isAdvancedUnlocked();
}

export function writeUnlock(record) {
    const payload = {
        unlocked: true,
        passedAt: new Date().toISOString(),
        ...record,
    };
    window.localStorage.setItem(UNLOCK_STORAGE_KEY, JSON.stringify(payload));
    return payload;
}

export function clearUnlock() {
    window.localStorage.removeItem(UNLOCK_STORAGE_KEY);
}

export function passedAlgebraCheck(correct, total) {
    if (!total) return false;
    return correct / total >= PASS_RATIO;
}

export function courseNameForLesson(plans, lesson) {
    if (!lesson) return null;
    if (lesson.courseName) return lesson.courseName;
    const id = lesson.id || lesson.metaId;
    if (!id || !Array.isArray(plans)) return null;
    for (const course of plans) {
        const lessons = course.lessons || [];
        if (lessons.some((item) => item.id === id || item.metaId === id)) {
            return course.courseName;
        }
        const metas = course.metaLessons || [];
        if (metas.some((item) => item.id === id)) {
            return course.courseName;
        }
    }
    return null;
}

function isOfficeHoursId(id) {
    return typeof id === "string" && id.startsWith("office-hours--");
}

export function courseIsFullyMastered(course, bktParams) {
    const lessons = (course?.lessons || []).filter(
        (lesson) => lesson && !lesson.officeHours && !isOfficeHoursId(lesson.id)
    );
    if (lessons.length === 0) return false;
    return lessons.every((lesson) => {
        const objectives = lesson.learningObjectives || {};
        const kcs = Object.keys(objectives);
        if (kcs.length === 0) return false;
        return kcs.every((kc) => {
            const threshold =
                typeof objectives[kc] === "number" && objectives[kc] > 0
                    ? objectives[kc]
                    : 0.85;
            const mastery = bktParams?.[kc]?.probMastery;
            return typeof mastery === "number" && mastery + 1e-9 >= threshold;
        });
    });
}

/**
 * Alternate unlock: mastery of every Elementary Algebra lesson.
 * Returns true when this call newly writes the unlock flag.
 */
export function maybeUnlockByElementaryMastery(plans, bktParams) {
    if (isAdvancedUnlocked()) return false;
    const course = (plans || []).find(
        (item) => item.courseName === ELEMENTARY_ALGEBRA_COURSE
    );
    if (!course || !courseIsFullyMastered(course, bktParams)) return false;
    writeUnlock({
        source: "elementary-mastery",
        score: 1,
        correct: null,
        total: null,
    });
    return true;
}
