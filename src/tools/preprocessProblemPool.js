const path = require("path");
const fs = require("fs");
const util = require('util');
const { CONTENT_SOURCE } = require('../../common/global-config')

const copyFile = util.promisify(fs.copyFile)
const readdir = util.promisify(fs.readdir)
const lstat = util.promisify(fs.lstat)
const writeFile = util.promisify(fs.writeFile)
const mkdir = util.promisify(fs.mkdir)
const rm = util.promisify(fs.rm)

if (+process.versions.node.split(".")[0] < 10) {
    console.debug('Please upgrade to node v10.12.X+')
    process.exit(1)
}

// the current file should be in src/tools so ../content-sources/* should be src/content-sources/*
const problemPoolPath = path.join(__dirname, '..', 'content-sources', CONTENT_SOURCE, 'content-pool')
const localPoolPath = path.join(__dirname, '..', 'local-content', 'prealgebra', 'content-pool')
const generatedPath = path.join(__dirname, '..', '..', 'generated', 'processed-content-pool')
const poolFilePath = path.join(generatedPath, `${CONTENT_SOURCE}.json`)
const publicContentDir = path.join(__dirname, '..', '..', 'public', 'static', 'content')
const publicPoolPath = path.join(publicContentDir, `${CONTENT_SOURCE}.json`)
const staticFiguresPath = path.join(__dirname, '..', '..', 'public', 'static', 'images', 'figures', CONTENT_SOURCE)

async function readPool(poolPath) {
    const updatedTime = -1;
    const directoryItems = await readdir(poolPath)
    const problemDirs = await Promise.all(directoryItems.map(async item => {
        const stat = await lstat(path.join(poolPath, item))
        let directory = ""
        if (stat.isDirectory()) {
            if (fs.lstatSync(path.join(poolPath, item)).mtime > updatedTime) {
                directory = item
            }
        }
        return directory
    })).catch(err => {
        console.debug(err)
        console.error('error reading problem directories')
        process.exit(1)
    })

    const problems = await Promise.all(
        problemDirs
            .filter(d => d.length > 0)
            .filter(d => !(d.toString().startsWith("_") || d.toString().startsWith(".")))
            .map(
                async problemDir => {
                    const problemName = problemDir.toString()
                    const problemPath = path.join(poolPath, problemName)

                    const problem = require(path.join(problemPath, `${problemName}.json`))

                    const stepDirs = await readdir(path.join(problemPath, 'steps'))
                    if (!stepDirs || stepDirs.length === 0) {
                        throw Error(`${problemName.toString()} has no steps.`)
                    }

                    const figurePaths = await readdir(path.join(problemPath, 'figures')).catch(() => {})
                    if (figurePaths && figurePaths.length > 0) {
                        await Promise.all(figurePaths.map(async figure => {
                            await mkdir(path.join(staticFiguresPath, problemDir.toString()), {
                                recursive: true
                            })
                            await copyFile(path.join(problemPath, 'figures', figure), path.join(staticFiguresPath, problemDir.toString(), figure))
                        }))
                    }

                    problem.steps = await Promise.all(
                        stepDirs.map(
                            async stepDir => {
                                const stepName = stepDir.toString()
                                const stepPath = path.join(problemPath, 'steps', stepName)

                                const step = require(path.join(stepPath, `${stepDir}.json`))

                                const hintPathwaysDir = await readdir(path.join(stepPath, 'tutoring')).catch(() => []) || []
                                if (hintPathwaysDir.length === 0) {
                                    console.warn(`${problemName} -> ${stepName} has no hints (pathways).`)
                                }

                                const hintPathways = await Promise.all(
                                    hintPathwaysDir.map(
                                        async hintPathwayFile => {
                                            const hintPathwayFullName = hintPathwayFile.toString()
                                            const hintPathwayPath = path.join(stepPath, 'tutoring', hintPathwayFullName)

                                            const hintPathway = require(hintPathwayPath)

                                            const hintPathwayName = hintPathwayFullName.includes(stepName)
                                                ? hintPathwayFullName.substr(hintPathwayFullName.indexOf(stepName) + stepName.length).replace(/\.[^/.]+$/, "")
                                                : hintPathwayFullName

                                            return { [hintPathwayName]: hintPathway }
                                        }))

                                step.hints = Object.fromEntries(hintPathways.map(obj => [Object.keys(obj)[0], obj[Object.keys(obj)[0]]]))
                                return step
                            }))

                    return problem
                })
    ).catch(err => {
        console.debug(err)
        console.error('error reading individual problem directory')
        process.exit(1)
    })

    return problems
}


;(async () => {
    await rm(staticFiguresPath, { recursive: true }).catch(err => {
        if (err && err.code !== 'ENOENT') {
            console.error('error removing existing figures')
            process.exit(1)
        }
    })

    const mainProblems = await readPool(problemPoolPath)
    const localProblems = fs.existsSync(localPoolPath) ? await readPool(localPoolPath) : []
    const config = mainProblems.concat(localProblems)
    console.log(`writing pool: ${mainProblems.length} content problems + ${localProblems.length} local problems`)

    await mkdir(generatedPath, { recursive: true })
    await mkdir(publicContentDir, { recursive: true })
    const payload = JSON.stringify(config)
    await writeFile(poolFilePath, payload)
    await writeFile(publicPoolPath, payload)
})()
