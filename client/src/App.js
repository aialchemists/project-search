import React, { useCallback, useEffect, useState } from 'react';
import styled from "styled-components";
import { Skeleton } from '@mui/material';

import { getConfigs } from './apis/configs';
import { search } from './apis/search';

import Header from './components/Header'
import SearchBox from './components/SearchBox';
import ResultPanel from './components/ResultPanel';
import MetaDataPanel from './components/MetaDataPanel';

const MainPanel = styled.section`
  padding: 40px 20px;

  .quote-text {
    margin-top: 40px;
    text-align: center;
    font-size: 0.8em;
    font-style: italic;
  }
`;

const PlaceholderResults = styled(Skeleton)`
  margin-top: 20px;
`;

const LOADING = Symbol();

function App() {
  const [configs, setConfigs] = useState(null);
  useEffect(() => {
    getConfigs(setConfigs)
  }, []);

  const [filters, setFilters] = useState({});

  const [searchResp, setResults] = useState(null);
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

    span {
      color: #008080;
    }
  `;

  const isLoading = searchResp === LOADING;

  return (
    <div className="App">
      <Header configs={configs} />
      <MainPanel>
        <SearchBox onSearch={onSearch} isLoading={isLoading} />
        {isLoading && <PlaceholderResults variant="rounded" height={100} />}

        {Array.isArray(searchResp && searchResp.results) ? (
          <>
            <MetaDataPanel searchResp={searchResp} filters={filters} onFiltersChange={setFilters}/>
            <div>
              {searchResp.results.map((result, index) => (
                <ResultPanel key={index} result={result} />
              ))}
            </div>
          </>
        ) : (
          <div className='quote-text'>
            At its most basic level semantic search applies meaning to the connections between the data in ways that allow a clearer understanding of them than we have ever had to date ― David Amerland
          </div>
        )}
      </MainPanel>
      <Footer>By <span><b>AI</b>Alchemists</span></Footer>
    </div>
  );
}

export default App;
