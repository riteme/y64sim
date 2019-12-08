import React from 'react'

import { withStyles } from '@material-ui/core/styles'

import {
  Tabs,
  Tab
} from '@material-ui/core'

const styles = theme => ({
  root: {
    display: 'flex',
    height: '100%'
  },
  tabs: {
    borderRight: `1px solid ${theme.palette.divider}`
  },
  tabIcon: {
    minWidth: 48
  },
  page: {
    width: '100%',
    padding: theme.spacing(1)
  }
})

function TabPanel(props) {
  return props.value === props.index && <div className={props.className}>{props.children}</div>;
}

// icons
// pages
class Pager extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      index: 0
    }
  }

  handleChange = (event, value) => {
    this.setState({
      index: value
    })
  }

  render() {
    const { classes } = this.props;

    return (
      <div className={classes.root}>
        <Tabs
          orientation="vertical"
          value={this.state.index}
          onChange={this.handleChange}
          className={classes.tabs}
        >
          {this.props.icons.map(
            icon => <Tab icon={icon} className={classes.tabIcon} />
          )}
        </Tabs>
        {this.props.pages.map(
          (page, index) => (
            <TabPanel
              value={this.state.index}
              index={index}
              className={classes.page}
            >
              {page}
            </TabPanel>
          )
        )}
      </div>
    )
  }
}

export default withStyles(styles)(Pager);