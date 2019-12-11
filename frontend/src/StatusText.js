import React from 'react'
import { makeStyles } from '@material-ui/core/styles'

const useStyles = makeStyles({
  green: {
    color: 'green'
  },
  red: {
    color: 'red'
  },
  grey: {
    color: 'grey'
  }
})

function StatusText({ state }) {
  const classes = useStyles();

  return {
    0: <span className={classes.grey}>Unknown</span>,
    1: <span className={classes.green}>Normal</span>,
    2: <span className={classes.red}>Invalid Instruction</span>,
    3: <span className={classes.red}>Memory Error</span>,
    4: <span className={classes.red}>Halt</span>,
    5: <span className={classes.red}>Stalled</span>
  }[state];
}

export default StatusText;