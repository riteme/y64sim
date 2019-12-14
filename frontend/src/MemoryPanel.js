import React from 'react'
import { makeStyles } from '@material-ui/core/styles'

import {
  Tooltip
 } from '@material-ui/core'
import { yellow } from '@material-ui/core/colors'

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
  highlight: {
    backgroundColor: yellow[300]
  },
  outlined: {
    outline: '2px solid red'
  }
}));

function Byte({
  byte, index, outlined, highlight, classes
}) {
  return (
    // <Tooltip title={`0x${index.toString(16)}`}>
      <span className={[
        classes.byte,
        outlined && classes.outlined,
        highlight && classes.highlight
      ].join(' ')}>{byte}</span>
    // </Tooltip>
  )
}

class MemoryNode extends React.Component {
  shouldComponentUpdate(nextProps) {
    const { node, old, rip } = this.props;
    return node === null || nextProps.node === null ||
      (node.left <= rip && rip <= node.right) ||
      (nextProps.node.left <= nextProps.rip && nextProps.rip <= nextProps.node.right) ||
      node.value !== nextProps.node.value ||
      (old && node.value !== old.value);
  }

  render() {
    const {
      node, old, rip, classes
    } = this.props;
    if (node === null)
      return null;

    if (node.left === node.right)
      return <Byte
        byte={node.literal}
        index={node.left}
        outlined={node.left === rip}
        highlight={old && node.value !== old.value}
        classes={classes}
      />;

    return (
      <React.Fragment>
        <MemoryNode
          node={node.lch}
          old={old && old.lch}
          rip={rip}
          classes={classes}
        />
        <MemoryNode
          node={node.rch}
          old={old && old.rch}
          rip={rip}
          classes={classes}
        />
      </React.Fragment>
    )
  }
}

function MemoryPanel({
  tree, old, rip
}) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <pre className={classes.pre}>
        <MemoryNode
          node={tree}
          old={old}
          rip={rip}
          classes={classes}
        />
      </pre>
    </div>
  )
}

export default MemoryPanel;