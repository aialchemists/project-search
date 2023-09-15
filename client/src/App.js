import React, { useCallback, useEffect, useState } from 'react';
import styled from "styled-components";
import { Skeleton } from '@mui/material';

import { getConfigs } from './apis/configs';
import { search } from './apis/search';

import Header from './components/Header'
import SearchBox from './components/SearchBox';
import ResultPanel from './components/ResultPanel';

const MainPanel = styled.section`
  padding: 40px 20px;
`;

const PlaceholderResults = styled(Skeleton)`
  margin-top: 20px;
`;

const MetaDataPanel = styled.div`
  margin-top: 20px;
  text-align: right;
  color: #777;
`;

const LOADING = Symbol();

function App() {
  const [configs, setConfigs] = useState(null);
  useEffect(() => {
    getConfigs(setConfigs)
  }, []);

  const [results, setResults] = useState(null);
  const onSearch = useCallback(async (query) => {
    if(query) {
      setResults(LOADING);
      setResults(await search(query));
    }
  }, []);

  const Footer = styled.div`
    position: fixed;
    bottom: 0;
    left: 0px;
    right: 0px;
    height: 20px;
    padding: 5px 20px;

    text-align: right;
    background-color: #DDD;
    font-size: 0.9em;
    color: #444;
  `;

  const isLoading = results === LOADING;

  return (
    <div className="App">
      <Header configs={configs} />
      <MainPanel>
        <SearchBox onSearch={onSearch} isLoading={isLoading} />
        {isLoading && <PlaceholderResults variant="rounded" height={100} />}

        {Array.isArray(results) && (
          <>
            <MetaDataPanel>{results.length} matching results</MetaDataPanel>
            <div>
              {results.map((result, index) => (
                <ResultPanel key={index} result={result} />
              ))}
            </div>
          </>
        )}
      </MainPanel>
      <Footer>By <b>AI</b>Alchemists</Footer>
    </div>
  );
}

export default App;
