import styled from "styled-components";

import { FormControl, InputLabel, MenuItem, Select } from "@mui/material";

const Container = styled.div`
  position: relative;
  margin-left: -8px;
  top: 4px;
  height: 50px;

  .result-count {
    position: absolute;
    top: 0px;
    right: 0px;
    margin-top: 20px;
    text-align: right;
    color: #777;
  }
`;

function FilterSelect({facet, value, onChange}) {
  const values = facet.values.filter(val => val)
  return (
    <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
      <InputLabel id="demo-select-small-label">{facet.title}</InputLabel>
      <Select
        value={value || ""}
        label={facet.title}
        onChange={e => onChange(e.target.value)}
      >
        {values.map((value, index) => <MenuItem value={value} key={index}>{value}</MenuItem>)}
      </Select>
    </FormControl>
  );
}

function MetaDataPanel({searchResp, filters, onFiltersChange}) {
  return (
    <Container>
      <div className="filters">
        {searchResp.facets.map(facet => (
          <FilterSelect
            facet={facet}
            value={filters[facet.title]}
            onChange={value => {
              onFiltersChange({
                ...filters,
                [facet.title]: value
              })
            }}
            key={facet.title}/>
        ))}
      </div>
      <div className="result-count">
        {searchResp.results.length} matching results
      </div>
    </Container>
  );
}

export default MetaDataPanel;
