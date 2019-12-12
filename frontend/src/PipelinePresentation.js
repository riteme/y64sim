import React from 'react'
import { makeStyles } from '@material-ui/core/styles'

import {
  IconButton, Typography, Fade, Tooltip
} from '@material-ui/core'

import RefreshIcon from '@material-ui/icons/Refresh'
import PlayArrowIcon from '@material-ui/icons/PlayArrow'
import PauseIcon from '@material-ui/icons/Pause'
import NavigateBeforeIcon from '@material-ui/icons/NavigateBefore'
import NavigateNextIcon from '@material-ui/icons/NavigateNext'

import InstructionPanel from './InstructionPanel'

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
  },
  control: {
    color: theme.palette.grey[700],
    borderBottom: `1px solid ${theme.palette.divider}`,
    padding: [[0, theme.spacing(0.5)]],
    display: 'flex',
    flexDirection: 'row',
    backgroundColor: theme.palette.common.white,
    transition: [
      theme.transitions.create('background'),
      theme.transitions.create('color')
    ],
    '& button': {
      transition: theme.transitions.create('color'),
      color: 'inherit'
    }
  },
  controlInError: {
    backgroundColor: theme.palette.error.light,
    color: theme.palette.common.white
  },
  controlButtons: {
    flexGrow: 1,
    flexBasis: '20%'
  },
  controlStatus: {
    display: 'flex',
    flexGrow: 1,
    flexBasis: '20%',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 'bold',
    color: 'inherit'
  },
  controlCycleDisplay: {
    display: 'flex',
    flexGrow: 1,
    flexBasis: '20%',
    alignItems: 'center',
    justifyContent: 'flex-end',
    paddingRight: theme.spacing(0.5),
    color: 'inherit'
  },
  pipeline: {
    height: '100%'
  }
}))

function PipelinePresentation({
  enabled,
  playing,
  frame,
  old,
  frameIndex,
  status,

  onReset,
  onStartPlay,
  onPause,
  onGoPrev,
  onGoNext
}) {
  const classes = useStyles();
  const inError = frame.state > 1;

  return (
    <div className={classes.root}>
      <div className={[
        classes.control,
        inError && classes.controlInError
      ].join(' ')}>
        <div className={classes.controlButtons}>
          <Tooltip title="Reset"><span>
            <IconButton
              size="small"
              disabled={!enabled || playing || frameIndex === 0}
              onClick={onReset}
            ><RefreshIcon /></IconButton>
          </span></Tooltip>
          { !playing ?
            <Tooltip title="Run"><span>
              <IconButton
                size="small"
                disabled={!enabled}
                onClick={onStartPlay}
              ><PlayArrowIcon /></IconButton>
            </span></Tooltip> :
            <Tooltip title="Pause"><span>
              <IconButton
                size="small"
                disabled={!enabled}
                onClick={onPause}
              ><PauseIcon /></IconButton>
            </span></Tooltip>
          }
          <Tooltip title="Previous"><span>
            <IconButton
              size="small"
              disabled={!enabled || playing || frameIndex === 0}
              onClick={onGoPrev}
            ><NavigateBeforeIcon /></IconButton>
          </span></Tooltip>
          <Tooltip title="Next"><span>
            <IconButton
              size="small"
              disabled={!enabled || playing}
              onClick={onGoNext}
            ><NavigateNextIcon /></IconButton>
          </span></Tooltip>
        </div>
        <div className={classes.controlStatus}>
          <Fade in={inError}>
            <Typography variant="body1">
              {status}
            </Typography>
          </Fade>
        </div>
        <div className={classes.controlCycleDisplay}>
          <Typography variant="body1">
            Cycle {frameIndex}
          </Typography>
        </div>
      </div>
      <div className={classes.pipeline}>
        <InstructionPanel
          stages={frame.stages}
          old={old.stages}
        />
      </div>
    </div>
  )
}

export default PipelinePresentation;