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
    backgroundColor: theme.palette.grey[200]
  },
  summary: {
    transition: [
      theme.transitions.create('background'),
      theme.transitions.create('color')
    ]
  },
  summaryDark: {
    backgroundColor: theme.palette.grey[200]
  },
  summaryLight: {
    color: [theme.palette.common.white, `!important`],
    backgroundColor: '#4dc8ab'
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
  regs
}) {
  const classes = useStyles();
  const light = literal !== '(no instruction)' && literal !== '';

  return (
    <ExpansionPanel
      elevation={0}
      classes={{rounded: classes.panel}}
    >
      <ExpansionPanelSummary
        expandIcon={<ExpandMoreIcon />}
        classes={{root: [
          classes.summary,
          light ? classes.summaryLight : classes.summaryDark
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
          data={regs}
          translateState
        />
      </ExpansionPanelDetails>
    </ExpansionPanel>
  )
}

function InstructionPanel({
  stages
}) {
  const classes = useStyles();

  if (stages === null || stages === undefined) {
    return (
      <div className={classes.root}>
        <Instruction name="WRITE" literal="(no instruction)" />
        <Instruction name="MEMORY" literal="(no instruction)" />
        <Instruction name="EXECUTE" literal="(no instruction)" />
        <Instruction name="DECODE" literal="(no instruction)" />
        <Instruction name="FETCH" literal="(no instruction)" />
      </div>
    )
  } else {
    return (
      <div className={classes.root}>
        <Instruction
          name="WRITE"
          literal={stages.write.instruction.literal}
          regs={stages.write.registers}
        />
        <Instruction
          name="MEMORY"
          literal={stages.memory.instruction.literal}
          regs={stages.memory.registers}
        />
        <Instruction
          name="EXECUTE"
          literal={stages.execute.instruction.literal}
          regs={stages.execute.registers}
        />
        <Instruction
          name="DECODE"
          literal={stages.decode.instruction.literal}
          regs={stages.decode.registers}
        />
        <Instruction
          name="FETCH"
          literal={stages.fetch.instruction.literal}
          regs={stages.fetch.registers}
        />
      </div>
    )
  }
}

export default InstructionPanel;