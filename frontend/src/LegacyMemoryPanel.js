import React from 'react'
import { withStyles } from '@material-ui/core/styles'

import {
  Tooltip
 } from '@material-ui/core'
import { yellow } from '@material-ui/core/colors'

const styles = theme => ({
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
  highlight: {
    backgroundColor: yellow[300]
  },
  outlined: {
    outline: '2px solid red'
  }
})

function Byte({
  byte, index, outlined, highlight, classes
}) {
  return (
    <Tooltip title={`0x${index.toString(16)}`}>
      <span className={[
        classes.byte,
        outlined && classes.outlined,
        highlight && classes.highlight
      ].join(' ')}>{byte}</span>
    </Tooltip>
  )
}

class LegacyMemoryPanel extends React.Component {
  shouldComponentUpdate(nextProps) {
    return (
      this.props.rip !== nextProps.rip ||
      this.props.memory !== nextProps.memory
    )
  }

  render() {
    const { memory, rip, old, classes } = this.props;

    return (
      <div className={classes.root}>
        <pre className={classes.pre}>
          {memory && memory.map((byte, index) =>
            <Byte
              key={index}
              index={index}
              byte={byte}
              outlined={index === rip}
              highlight={old[index] && old[index] !== byte}
              classes={classes}
            />
          )}
        </pre>
      </div>
    )
  }
}

export default withStyles(styles)(LegacyMemoryPanel);