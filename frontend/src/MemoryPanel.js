import React from 'react'
import { makeStyles } from '@material-ui/core/styles'

import {
  Typography,
  Tooltip
 } from '@material-ui/core'

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    height: '100%'
  },
  pre: {
    padding: theme.spacing(0.5),
    backgroundColor: theme.palette.background.default,
    overflow: 'auto',
    height: '100%',
    width: '100%',
    margin: 0,
    fontSize: '1.07rem',
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'flex-start',
    alignContent: 'baseline'
  },
  byte: {
    height: 'min-content',
    wordBreak: 'keep-all',
    padding: [[0, theme.spacing(0.5)]],
    outlineColor: theme.palette.background.default,
    transition: theme.transitions.create('outline-color'),
    '&:hover': {
      backgroundColor: theme.palette.grey[300]
    }
  },
  byteUpdated: {
    backgroundColor: 'yellow'
  },
  rip: {
    outline: '2px solid red'
  }
}))

function Byte({
  byte, index, rip, old
}) {
  const classes = useStyles();
  return (
    <Tooltip key={index} title={`Location: 0x${index.toString(16)}`}>
      <span className={[
        classes.byte,
        index === rip ? classes.rip : null,
        old && old !== byte ? classes.byteUpdated : null
      ].join(' ')}>{byte}</span>
    </Tooltip>
  )
}

function MemoryPanel({
  memory, rip, old
}) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <pre className={classes.pre}>
        {memory && memory.map((byte, index) =>
          <Byte
            key={index}
            byte={byte}
            old={old === null ? null : old[index]}
            index={index}
            rip={rip}
          />
        )}
      </pre>
    </div>
  )
}

export default MemoryPanel;