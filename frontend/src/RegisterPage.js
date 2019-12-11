import React from 'react'
import { makeStyles } from '@material-ui/core/styles'

import {
  ExpansionPanel,
  ExpansionPanelSummary,
  ExpansionPanelDetails,
  Typography
} from '@material-ui/core'

import ExpandMoreIcon from '@material-ui/icons/ExpandMore'

import RegisterPanel from './RegisterPanel'
import StatusText from './StatusText'

const useStyles = makeStyles(theme => ({
  root: {
    height: '100%',
    overflow: 'auto'
  },
  panel: {
    margin: [theme.spacing(1.5), '!important'],
    borderRadius: '0 !important',
    backgroundColor: theme.palette.grey[200]
  },
  core: {
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
  },
  line: {
    display: 'flex'
  },
  coreTitle: {
    flexBasis: '30%',
    flexShrink: 0,
    textAlign: 'right'
  },
  coreValue: {
    flexGrow: 1,
    textAlign: 'right'
  },
  na: {
    color: theme.palette.text.hint
  },
  details: {
    padding: 0
  }
}))

function CoreStates({
  rip, state
}) {
  const classes = useStyles();

  if (rip === null || state === null) return (
    <Typography variant="body1" className={classes.na}>Not Available</Typography>
  );

  return (
    <div className={classes.core}>
      <div className={classes.line}>
        <Typography variant="subtitle1" className={classes.coreTitle}>Program Counter:</Typography>
        <Typography variant="subtitle1" className={classes.coreValue}>{`0x${rip.toString(16)}`}</Typography>
      </div>
      <div className={classes.line}>
        <Typography variant="subtitle1" className={classes.coreTitle}>Processor Status:</Typography>
        <Typography variant="subtitle1" className={classes.coreValue}>
          <StatusText state={state} />
        </Typography>
      </div>
    </div>
  )
}

function RegisterPage({
  rip, state, file, cc
}) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <ExpansionPanel
        elevation={0}
        classes={{rounded: classes.panel}}
        defaultExpanded
      >
        <ExpansionPanelSummary
          expandIcon={<ExpandMoreIcon />}
        >
          <Typography variant="subtitle1">
            CORE STATUS
          </Typography>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails>
          <CoreStates rip={rip} state={state} />
        </ExpansionPanelDetails>
      </ExpansionPanel>
      <ExpansionPanel
        elevation={0}
        classes={{rounded: classes.panel}}
        defaultExpanded
      >
        <ExpansionPanelSummary
          expandIcon={<ExpandMoreIcon />}
        >
          <Typography variant="subtitle1">
            REGISTER FILE
          </Typography>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails classes={{root: classes.details}}>
          <RegisterPanel data={file} />
        </ExpansionPanelDetails>
      </ExpansionPanel>
      <ExpansionPanel
        elevation={0}
        classes={{rounded: classes.panel}}
        defaultExpanded
      >
        <ExpansionPanelSummary
          expandIcon={<ExpandMoreIcon />}
        >
          <Typography variant="subtitle1">
            CONDITION CODES
          </Typography>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails classes={{root: classes.details}}>
          <RegisterPanel data={cc} />
        </ExpansionPanelDetails>
      </ExpansionPanel>
    </div>
  )
}

export default RegisterPage;