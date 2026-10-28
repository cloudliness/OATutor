/**
 * OATutor lesson text lives in the public OATutor-Content repo, recorded as
 * a git submodule. Vercel can clone that submodule; this script also clones
 * it directly when the checkout is empty, and pins the commit this fork was
 * built against.
 */
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const root = path.join(__dirname, "..");
const dest = path.join(root, "src", "content-sources", "oatutor");
const marker = path.join(dest, "coursePlans.json");
const pool = path.join(dest, "content-pool");
const PIN = "1925decc91567faf6203bdb41b9d52b14891426f";
const REMOTE = "https://github.com/CAHLR/OATutor-Content.git";

function ready() {
    return fs.existsSync(marker) && fs.existsSync(pool);
}

function run(command, cwd = root) {
    execSync(command, { stdio: "inherit", cwd });
}

if (ready()) {
    console.log("[ensure-content] OATutor-Content is already present.");
    process.exit(0);
}

console.log("[ensure-content] Fetching OATutor-Content...");

try {
    run("git submodule update --init --depth 1 src/content-sources/oatutor");
} catch (err) {
    console.warn("[ensure-content] git submodule update failed; cloning directly.");
}

if (!ready()) {
    fs.rmSync(dest, { recursive: true, force: true });
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    run(`git clone ${REMOTE} "${dest}"`);
    try {
        run(`git fetch --depth 1 origin ${PIN}`, dest);
        run(`git checkout ${PIN}`, dest);
    } catch (err) {
        console.warn(
            "[ensure-content] Could not check out the pinned content commit; using the default branch."
        );
    }
}

if (!ready()) {
    console.error("[ensure-content] coursePlans.json is still missing.");
    process.exit(1);
}

console.log("[ensure-content] Content is ready.");
