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

const useStyles = makeStyles(theme => ({
  root: {
    height: '100%',
    overflow: 'auto'
  },
  panel: {
    margin: [theme.spacing(1.5), '!important'],
    borderRadius: '0 !important',
    backgroundColor: theme.palette.grey[100],
    '&:before': {
      display: 'none'
    }
  },
  summary: {
    transition: [
      theme.transitions.create('background'),
      theme.transitions.create('color')
    ]
  },
  summaryDark: {
    backgroundColor: theme.palette.grey[100]
  },
  summaryLight: {
    color: [theme.palette.common.white, `!important`],
    backgroundColor: '#4dc8ab'
  },
  summaryError: {
    color: [theme.palette.common.white, `!important`],
    backgroundColor: theme.palette.error.light
  },
  stageNameDiv: {
    flexBasis: '16%',
    flexShrink: 0
  },
  instructionDiv: {
    display: 'flex',
    alignItems: 'flex-end'
  },
  instruction: {
    fontSize: theme.typography.h6.fontSize,
    color: theme.palette.text.secondary
  },
  details: {
    padding: 0
  }
}))

function Instruction({
  name,
  literal,
  registers,
  old_registers,
  variant
}) {
  const classes = useStyles();
  const summaryClass = {
    'none': classes.summaryDark,
    'light': classes.summaryLight,
    'error': classes.summaryError
  }[variant];

  return (
    <ExpansionPanel
      elevation={0}
      classes={{rounded: classes.panel}}
    >
      <ExpansionPanelSummary
        expandIcon={<ExpandMoreIcon />}
        classes={{root: [
          classes.summary, summaryClass
        ].join(' ')}}
      >
        <div className={classes.stageNameDiv}>
          <Typography variant="subtitle1">{name}</Typography>
        </div>
        <div className={classes.instructionDiv}>
          <code className={classes.instruction}>{literal}</code>
        </div>
      </ExpansionPanelSummary>
      <ExpansionPanelDetails classes={{root: classes.details}}>
        <RegisterPanel
          data={registers}
          old={old_registers}
          translateState
        />
      </ExpansionPanelDetails>
    </ExpansionPanel>
  )
}

function InstructionPanel({
  stages,
  old
}) {
  const classes = useStyles();
  const names = [
    'write',
    'memory',
    'execute',
    'decode',
    'fetch'
  ];

  return (
    <div className={classes.root}>
      {names.map(name => {
        const stage = stages[name];
        const literal = stage.instruction.literal;

        return <Instruction
          key={name}
          name={name.toUpperCase()}
          literal={literal}
          registers={stage.registers}
          old_registers={old[name].registers}
          variant={
            stage.registers === null || literal === '(no instruction)' ?
              'none' : (
                stage.registers.state[0] === 1 ?
                  'light' : 'error'
              )
          }
        />;
      })}
    </div>
  )
}

export default InstructionPanel;