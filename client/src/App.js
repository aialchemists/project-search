import React, { useCallback, useEffect, useState } from 'react';
import styled from "styled-components";

import Header from './components/Header'

import { getConfigs } from './apis/configs';
import { search } from './apis/search';

import SearchBox from './components/SearchBox';
import { Skeleton } from '@mui/material';

const MainPanel = styled.section`
  padding: 40px 20px;
`;

const ResultPanel = styled.div`
  background-color: #DDDD;
  border-radius: 5px;
  margin: 20px 0;
  padding: 10px;
`;

const PlaceholderResults = styled(Skeleton)`
  margin-top: 20px;
`;

const SourceLink = styled.a`
  font-size: 0.8em;

  display: inline-block;
  margin-top: 5px;
  color: #008080;
`;

const LOADING = Symbol();

function getFileName(path) {
  const parts = path.split("/");
  return parts[parts.length - 1];
}

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

  const isLoading = results === LOADING;

  console.log(results)

  return (
    <div className="App">
      <Header configs={configs} />
      <MainPanel>
        <SearchBox onSearch={onSearch} isLoading={isLoading} />
        {isLoading && <PlaceholderResults variant="rounded" height={100} />}

        {Array.isArray(results) && (
          <div>
            {
              results.map((result, index) => (
                <ResultPanel key={index}>
                  <div>{result.text}</div>
                  <SourceLink href={result.file_path} target='_blank'>{getFileName(result.file_path)}</SourceLink>
                </ResultPanel>
              ))
            }
          </div>
        )}
      </MainPanel>
    </div>
  );
}

export default App;
