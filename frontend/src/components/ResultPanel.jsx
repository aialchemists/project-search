import styled from "styled-components";
import CircularProgressWithLabel from "./CircularProgressWithLabel";

import SmartToyIcon from '@mui/icons-material/SmartToy';
import ListIcon from '@mui/icons-material/List';

const Container = styled.div`
  position: relative;
  background-color: #DDD7;
  border-radius: 5px;
  margin: 20px 0;
  padding: 10px;
  padding-right: 80px;

  img {
    height: 50px;
    border-radius: 5px;
    border: 1px solid #666;
  }

  .icons {
    display: inline-block;
    vertical-align: sub;
    > * {
      margin-right: 5px;
    }
  }

  .score-value {
    position: absolute;
    top: 10px;
    right: 10px;
    color: #008080;
    font-size: 2em;
  }
`;

const SourceLink = styled.a`
  font-size: 0.8em;

  display: inline-block;
  margin-top: 5px;
  color: #008080;

  font-weight: bold;
`;

const MAX_TEXT_LENGTH = 500;

// TODO: Do this using pure CSS
function getChunkText(text) {
  if(text.length > MAX_TEXT_LENGTH) {
    text = text.slice(0, MAX_TEXT_LENGTH) + "...";
  }
  return text;
}

function getFileName(path) {
  const parts = path.split("/");
  return parts[parts.length - 1];
}

function ResultPanel({result}) {
  const file_path = `/files/${result.file_path}`
  return (
    <Container>
      <div className="chunk-content">
        {result.file_type === "image" ? (
            <SourceLink href={file_path} target='_blank'><img src={file_path} alt={result.text} /></SourceLink>
        ) : (
          <span>{getChunkText(result.text)}</span>
        )}
      </div>
      <div className="icons">
        {result["semantic_match"] && (
          <SmartToyIcon fontSize="12" color="primary" titleAccess="Semantic Match" />
        )}
        {result["lexical_match"] && (
          <ListIcon fontSize="12" color="secondary" titleAccess="Lexical Match" />
        )}
      </div>
      <SourceLink href={file_path} target='_blank'>{getFileName(result.file_path)}</SourceLink>
      <div className="score-value">
        <CircularProgressWithLabel value={result.score * 100} />
      </div>
    </Container>
  );
}

export default ResultPanel;
