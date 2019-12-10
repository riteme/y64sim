import React from 'react'
import { withStyles } from '@material-ui/core/styles'

import {
  Box, Typography
} from '@material-ui/core'

const styles = theme => ({
  heading: {
    padding: theme.spacing(0.5),
    color: theme.palette.grey[600],
    borderBottom: `1px solid ${theme.palette.divider}`
  },
  pre: {
    overflow: 'auto',
    padding: [[0, theme.spacing(0.5)]],
    margin: 0,
    fontSize: theme.typography.htmlFontSize,
    backgroundColor: theme.palette.grey[100]
  },
  message: {
    wordBreak: 'break-all',
    whiteSpace: 'pre-line'
  }
})

class LoggingTerminal extends React.Component {
  constructor(props) {
    super(props);
    this.pre = React.createRef();
  }

  componentDidUpdate() {
    this.pre.current.scrollTop = this.pre.current.scrollHeight;
  }

  render() {
    const { classes } = this.props;

    return (
      <div>
        <div className={classes.heading}>
          <Typography variant="subtitle2">CONSOLE OUTPUT</Typography>
        </div>
        <div>
          <Box
            ref={this.pre}
            component="pre"
            height={this.props.height}
            classes={{root: classes.pre}}
          >
            {this.props.messages.map((element, index) => (
              <span key={index} className={classes.message}>{element}<br /></span>
            ))}
          </Box>
        </div>
      </div>
    )
  }
}

export default withStyles(styles)(LoggingTerminal);