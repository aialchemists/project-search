import { useState } from 'react';

import styled from "styled-components";

import SettingsIcon from '@mui/icons-material/Settings';
import IconButton from '@mui/material/IconButton';
import Popover from '@mui/material/Popover';

const HeaderPanel = styled.header`
  height: 20px;
  background-color: #DDD;
  box-shadow: 0 4px 5px -2px #DDDA;
  padding: 10px 20px;

  img {
    opacity: 0.8;
  }

  .logo-text {
    vertical-align: top;
    margin-left: 5px;
  }

  .icon-panel {
    position: absolute;
    right: 0px;
    top: 0px;
    padding: 3px 20px;
  }
`;

const ConfigurationsPanel = styled.div`
  padding: 10px;
`;

function Header(configs) {
  const [settingsElm, setSettingsElm] = useState(null);

  return (
    <HeaderPanel>
      <img src="favicon.ico" width="20" alt="logo" />
      <span className="logo-text">
        Vector Search
      </span>
      <div className="icon-panel">
        <IconButton size="small" onClick={event => setSettingsElm(event.currentTarget)}>
          <SettingsIcon />
        </IconButton>
        <Popover
          open={Boolean(settingsElm)}
          anchorEl={settingsElm}
          onClose={() => setSettingsElm(null)}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'left',
          }}
        >
          <ConfigurationsPanel  >
            <pre>
              {JSON.stringify(configs, null, 2) }
            </pre>
          </ConfigurationsPanel>
        </Popover>
      </div>
    </HeaderPanel>
  );
}

export default Header;
