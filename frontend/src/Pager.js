import React from 'react'

import { makeStyles } from '@material-ui/core/styles'

import {
  Tabs,
  Tab
} from '@material-ui/core'

const useStyles = makeStyles(theme => ({
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
    width: '100%'
  }
}))

function TabPanel(props) {
  return props.value === props.index && <div className={props.className}>{props.children}</div>;
}

// icons
// pages
function Pager(props) {
  const [state, setState] = React.useState({
    index: 0
  })

  const handleChange = (event, value) => {
    setState({
      index: value
    })
  }

  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Tabs
        orientation="vertical"
        value={state.index}
        onChange={handleChange}
        className={classes.tabs}
      >
        {props.icons.map(
          (icon, index) => <Tab icon={icon} key={index} className={classes.tabIcon} />
        )}
      </Tabs>
      {props.pages.map(
        (page, index) => (
          <TabPanel
            value={state.index}
            index={index}
            key={index}
            className={classes.page}
          >
            {page}
          </TabPanel>
        )
      )}
    </div>
  )
}

export default Pager;