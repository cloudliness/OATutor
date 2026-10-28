import React, { Fragment } from 'react';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import Divider from '@material-ui/core/Divider';
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';
import styles from './common-styles.js';
import IconButton from '@material-ui/core/IconButton';
import { _coursePlansNoEditor, ThemeContext, SITE_NAME, SHOW_COPYRIGHT } from '../../config/config.js';
import { isFullChatLesson } from '../../util/officeHours.js';
import Spacer from "../Spacer";
import { Typography } from "@material-ui/core";
import { IS_STAGING_OR_DEVELOPMENT } from "../../util/getBuildType";
import BuildTimeIndicator from "@components/BuildTimeIndicator";
import withTranslation from "../../util/withTranslation.js";
import MenuBookIcon from '@material-ui/icons/MenuBook';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import {
    PREALGEBRA_COURSE,
    clearUnlock,
    isAdvancedUnlocked,
    isCourseUnlocked,
} from '../../course-gate/courseAccess';
import { LocalizationConsumer } from '../../util/LocalizationContext';
import { withResponsive } from '../../util/ResponsiveContext';

class LessonSelection extends React.Component {
    static contextType = ThemeContext;

    constructor(props, context) {
        super(props);

        this.user = context.user || {}
        this.isPrivileged = !!this.user.privileged

        this.coursePlans = _coursePlansNoEditor;

        this.state = {
            preparedRemoveProgress: false,
            removedProgress: false,
            unlockVersion: 0,
        }
    }

    resetCourseUnlock = () => {
        clearUnlock();
        this.setState({ unlockVersion: Date.now() });
    }
      
    removeProgress = () => {
        this.setState({ removedProgress: true });
        this.props.removeProgress();
    }

    prepareRemoveProgress = () => {
        this.setState({ preparedRemoveProgress: true });
    }

    handleCourseSelect = (course, courseIndex) => {
        const { history } = this.props;
        // localStorage.setItem("defaultLocale", course.language); 

        history.push(`/courses/${courseIndex}`);
    };

    render() {
        const { translate } = this.props;
        const { classes, courseNum } = this.props;
        const isMobile = this.props.responsive?.isMobile ?? false;
        const selectionMode = courseNum == null ? "course" : "lesson"

        const advancedUnlocked = isAdvancedUnlocked();
        if (selectionMode === "lesson" && courseNum >= this.coursePlans.length) {
            return <Box width={'100%'} textAlign={'center'} pt={4} pb={4}>
                <Typography variant={'h3'}>Course <code>{courseNum}</code> is not valid!</Typography>
            </Box>
        }

        if (selectionMode === "lesson" && !isCourseUnlocked(this.coursePlans[courseNum]?.courseName)) {
            return <Box width={'100%'} textAlign={'center'} pt={4} pb={4} px={2}>
                <LockOutlinedIcon style={{ fontSize: 48 }} />
                <Typography variant={'h4'} style={{ marginTop: 12 }}>Pass the Algebra Check to unlock</Typography>
                <Box mt={3}>
                    <Button variant="contained" color="primary" onClick={() => this.props.history.push("/algebra-check")}>
                        Take the Algebra Check
                    </Button>
                </Box>
                <Box mt={2}>
                    <Button onClick={() => this.props.history.push("/")}>Back to courses</Button>
                </Box>
            </Box>
        }

        return (
            <>
                <div>
                    <Grid
                        container
                        spacing={0}
                        direction="column"
                        alignItems="center"
                        justifyContent="center"
                    >
                        <Box
                            width={isMobile ? "100%" : "75%"}
                            maxWidth={1500}
                            style={isMobile ? { paddingLeft: 16, paddingRight: 16 } : undefined}
                            role={"main"}
                        >
                            <center>
                                {this.isPrivileged
                                    ? <h1>{translate('lessonSelection.welcomeInstructor')}</h1>
                                    : <h1>{translate('lessonSelection.welcomeTo')} {SITE_NAME.replace(/\s/, "")}!</h1>
                                }

                                <h2>{translate('lessonSelection.select')} {selectionMode === "course" ? translate('lessonSelection.course') : translate('lessonSelection.lessonplan')}</h2>
                                {this.isPrivileged
                                    && <h4>(for {this.user.resource_link_title})</h4>
                                }
                                {
                                    IS_STAGING_OR_DEVELOPMENT && <BuildTimeIndicator/>
                                }
                            </center>
                            <Divider/>
                            <Spacer/>
                            {selectionMode === "course" && (
                                <Box mb={2} px={1}>
                                    <Typography variant="body1" style={{ fontSize: 16, lineHeight: 1.5, textAlign: "center" }}>
                                        Recommended: start with Pre-Algebra, then Elementary Algebra.
                                        {" "}
                                        {advancedUnlocked
                                            ? "Advanced courses are unlocked on this browser."
                                            : "Other courses stay locked until you pass the Algebra Check at 80%, or master every Elementary Algebra lesson."}
                                    </Typography>
                                    {!advancedUnlocked && (
                                        <Box mt={1} display="flex" justifyContent="center">
                                            <Button variant="contained" color="primary" onClick={() => this.props.history.push("/algebra-check")}>
                                                Algebra Check
                                            </Button>
                                        </Box>
                                    )}
                                </Box>
                            )}
                            <Grid container spacing={3}>
                                {selectionMode === "course"
                                    ? this.coursePlans
                                        .map((course, i) => {
                                            const unlocked = isCourseUnlocked(course.courseName);
                                            return (
                                            <Grid item xs={12} sm={6} md={4} key={course.courseName}>
                                                <center>
                                                    <Paper className={classes.paper} style={{ fontSize: "1rem", textAlign: "center", paddingBottom: 12 }}>
                                                        <h2 style={{
                                                            minHeight: "2.5em",
                                                            marginTop: "0.2em",
                                                            marginBottom: "0.4em",
                                                            textAlign: "center",
                                                            display: "flex",
                                                            alignItems: "center",
                                                            justifyContent: "center",
                                                            wordBreak: "break-word",
                                                        }}>{course.courseName}</h2>
                                                        {course.courseName === PREALGEBRA_COURSE && (
                                                            <Typography variant="body2" style={{ color: "#1f4b6e", fontWeight: 600, marginBottom: 8 }}>
                                                                Recommended: start with Pre-Algebra
                                                            </Typography>
                                                        )}
                                                        {unlocked ? (
                                                        <IconButton aria-label={`View Course ${course.courseName}`}
                                                            role={"link"}
                                                            onClick={() => {
                                                                this.props.selectCourse(course);
                                                                this.props.history.push(`/courses/${i}`)
                                                            }}>
                                                            <img
                                                                src={`${process.env.PUBLIC_URL}/static/images/icons/folder_outline_2.svg`}
                                                                alt=""
                                                                style= {{ width: "2.6em" }}
                                                            />
                                                        </IconButton>
                                                        ) : (
                                                            <div>
                                                                <LockOutlinedIcon aria-hidden="true" style={{ fontSize: 36, color: "#5c6b7a" }} />
                                                                <Typography variant="body2" style={{ marginTop: 8, padding: "0 8px" }}>
                                                                    Pass the Algebra Check to unlock
                                                                </Typography>
                                                            </div>
                                                        )}
                                                    </Paper>
                                                </center>
                                            </Grid>
                                            );
                                        })
                                    : (() => {
                                        const course = this.coursePlans[this.props.courseNum];
                                        const metaLessons = Array.isArray(course.metaLessons) ? course.metaLessons : [];

                                        const metaLessonChildIds = new Set();
                                        metaLessons.forEach((m) => {
                                            (Array.isArray(m.lessons) ? m.lessons : []).forEach((childId) => metaLessonChildIds.add(childId));
                                        });

                                        // Students should only reach A/B variants through the meta-lesson, which
                                        // handles branch assignment. Selecting a variant directly would bypass it.
                                        // Lessons not referenced by any meta-lesson still show normally.
                                        const visibleLessons = course.lessons.filter(
                                            (lesson) => !metaLessonChildIds.has(lesson.metaId) && !metaLessonChildIds.has(lesson.id)
                                        );

                                        return (
                                            <Fragment>
                                                {visibleLessons.map((lesson, i) => {
                                        return (
                                            <Grid item xs={12} sm={6} md={4} key={i}>
                                            <center>
                                            <Paper className={classes.paper} style={{ position: "relative", height: "12rem" }}>
                                                {!isFullChatLesson(lesson) && (
                                                <IconButton
                                                    size="small"
                                                    style={{ position: 'absolute', top: 8, right: 8 }}
                                                    aria-label={`View all problems for lesson ${lesson.id}`}
                                                    onClick={() => this.props.history.push(`/lessons/${lesson.id}/problems`)}
                                                >
                                                    <MenuBookIcon fontSize="small" />
                                                </IconButton>
                                                )}

                                                <div
                                                    style={{
                                                        height: "2.5em",
                                                        marginTop: 5,
                                                        marginBottom: 10,
                                                        display: "flex",
                                                        alignItems: "center",
                                                        justifyContent: "center",
                                                        textAlign: "center",
                                                    }}
                                                >
                                                    <h2 style={{ margin: 0 }}>{lesson.name.replace(/##/g, "")}</h2>
                                                </div>

                                                <div
                                                    style={{
                                                        height: "2em",
                                                        marginTop: 5,
                                                        display: "flex",
                                                        alignItems: "center",
                                                        justifyContent: "center",
                                                        textAlign: "center",
                                                    }}
                                                >
                                                    {lesson.topics ? <h3 style={{ margin: 0 }}>{lesson.topics}</h3> : null}
                                                </div>

                                                <Button
                                                    variant="contained"
                                                    color="primary"
                                                    className={classes.button}
                                                    style={{
                                                        width: "8em",
                                                        position: "absolute",
                                                        bottom: "1.2em",
                                                        left: "50%",
                                                        transform: "translateX(-50%)"
                                                    }}
                                                    onClick={() => this.props.history.push(`/lessons/${lesson.id}`)}
                                                >
                                                    {translate('lessonSelection.onlyselect')}
                                                </Button>
                                            </Paper>
                                            </center>
                                        </Grid>
                                        )
                                    })}
                                                {metaLessons.length > 0 && (
                                                    <Fragment>
                                                        <Grid item xs={12}>
                                                            <Typography variant="h5" component="h3" style={{ marginTop: 16, marginBottom: 8 }}>Meta Lessons</Typography>
                                                        </Grid>
                                                        {metaLessons.map((metaLesson) => (
                                                            <Grid item xs={12} sm={6} md={4} key={metaLesson.id}>
                                                                <center>
                                                                    <Paper className={classes.paper} style={{ position: "relative", height: "12rem" }}>
                                                                        <div
                                                                            style={{
                                                                                height: "2.5em",
                                                                                marginTop: 5,
                                                                                marginBottom: 10,
                                                                                display: "flex",
                                                                                alignItems: "center",
                                                                                justifyContent: "center",
                                                                                textAlign: "center",
                                                                            }}
                                                                        >
                                                                            <h2 style={{ margin: 0 }}>{metaLesson.name || metaLesson.id}</h2>
                                                                        </div>

                                                                        <div
                                                                            style={{
                                                                                height: "2em",
                                                                                marginTop: 5,
                                                                                display: "flex",
                                                                                alignItems: "center",
                                                                                justifyContent: "center",
                                                                                textAlign: "center",
                                                                            }}
                                                                        >
                                                                            <h3 style={{ margin: 0, color: "#5F6368" }}>Meta lesson</h3>
                                                                        </div>

                                                                        <Button
                                                                            variant="contained"
                                                                            color="primary"
                                                                            className={classes.button}
                                                                            style={{
                                                                                width: "8em",
                                                                                position: "absolute",
                                                                                bottom: "1.2em",
                                                                                left: "50%",
                                                                                transform: "translateX(-50%)"
                                                                            }}
                                                                            onClick={() => this.props.history.push(`/lessons/${metaLesson.id}`)}
                                                                        >
                                                                            {translate('lessonSelection.onlyselect')}
                                                                        </Button>
                                                                    </Paper>
                                                                </center>
                                                            </Grid>
                                                        ))}
                                                    </Fragment>
                                                )}
                                            </Fragment>
                                        );
                                    })()
                                }
                            </Grid>
                            <Spacer/>
                        </Box>
                    </Grid>
                    <Spacer/>
                    <Grid container spacing={0}>
                        <Grid item xs={3} sm={3} md={5} key={1}/>
                        {!this.isPrivileged && <Grid item xs={12} sm={8} md={4} key={2}>
                            {this.state.preparedRemoveProgress ?
                                <Button className={classes.button} size="small"
                                        style={{ 
                                            width: "100%", 
                                            color: "#3F7091",
                                            backgroundColor: "transparent",
                                            border: "1px solid #4F86A8",
                                            boxShadow: "none"
                                        }} 
                                    onClick={this.removeProgress}
                                    disabled={this.state.removedProgress}>{this.state.removedProgress ? translate('lessonSelection.reset') : translate('lessonSelection.aresure')}</Button> :
                                <Button className={classes.button} size="small"
                                    style={{ 
                                        width: "100%", 
                                        color: "#3F7091",
                                        backgroundColor: "transparent",
                                        border: "1px solid #4F86A8",
                                        boxShadow: "none"
                                    }} 
                                    onClick={this.prepareRemoveProgress}
                                    disabled={this.state.preparedRemoveProgress}>{translate('lessonSelection.resetprogress')}</Button>}
                            <Button className={classes.button} size="small"
                                style={{
                                    width: "100%",
                                    marginTop: 8,
                                    color: "#3F7091",
                                    backgroundColor: "transparent",
                                    border: "1px solid #4F86A8",
                                    boxShadow: "none"
                                }}
                                onClick={this.resetCourseUnlock}
                                disabled={!advancedUnlocked}
                            >
                                Reset course unlock
                            </Button>
                        </Grid>}
                        <Grid item xs={3} sm={3} md={4} key={3}/>
                    </Grid>
                    <Spacer/>
                </div>



                <footer>
                    <div style={{ display: "flex", flexDirection: "row", alignItems: "center" }}>
                        <div style={{ marginLeft: 20, fontSize: 16 }}>
                            {SHOW_COPYRIGHT && <>© {new Date().getFullYear()} {SITE_NAME}</>}
                        </div>
                    </div>
                </footer>




            </>
        )
    }
}

// export default withStyles(styles)(withTranslation(LessonSelection));

export default withStyles(styles)(withResponsive(withTranslation((props) => (
    <LocalizationConsumer>
        {({ language, platformLanguage }) => (
            <LessonSelection
                {...props}
                language={language}
                platformLanguage={platformLanguage}
            />
        )}
    </LocalizationConsumer>
))));