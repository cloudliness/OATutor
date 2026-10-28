import { CONTENT_SOURCE } from "@common/global-config";

let pending = null;

export function problemPoolUrl() {
    const base = process.env.PUBLIC_URL || "";
    return `${base}/static/content/${CONTENT_SOURCE}.json`;
}

/**
 * The processed pool is a static file, not a webpack import, so the phone
 * does not have to parse a multi-megabyte JavaScript bundle before the
 * course list can render.
 */
export function loadProblemPool() {
    if (!pending) {
        pending = fetch(problemPoolUrl()).then(async (response) => {
            if (!response.ok) {
                throw new Error(
                    `Lesson content could not be loaded (${response.status}).`
                );
            }
            const data = await response.json();
            if (!Array.isArray(data)) {
                throw new Error("Lesson content was not a list of problems.");
            }
            return data;
        });
    }
    return pending;
}
