import { useState } from 'react';

import IconButton from "@mui/material/IconButton";
import InputAdornment from "@mui/material/InputAdornment";
import SearchIcon from '@mui/icons-material/Search';
import { TextField } from "@mui/material";

function SearchBox({onSearch}) {
  const [text, setText] = useState("");

  return (
    <TextField
      label="Search"
      fullWidth={true}
      value={text}
      onChange={e => setText(e.target.value)}
      onKeyDown={e => e.key === 'Enter' && onSearch(text)}
      InputProps={{
        endAdornment: (
          <InputAdornment position="end">
            <IconButton onClick={() => onSearch(text)}>
              <SearchIcon />
            </IconButton>
          </InputAdornment>
        )
      }}
    />
  );
}

export default SearchBox;
