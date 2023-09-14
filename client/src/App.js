import React, { useEffect, useState } from 'react';

import Header from './components/Header'

import { getConfigs } from './apis/configs';

function App() {
  const [configs, setConfigs] = useState(null);
  useEffect(() => {
    getConfigs(setConfigs)
  }, []);

  return (
    <div className="App">
      <Header configs={configs} />
    </div>
  );
}

export default App;
