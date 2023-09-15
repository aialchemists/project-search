import styled from "styled-components";

const Container = styled.div`
  position: relative;
  background-color: #DDDD;
  border-radius: 5px;
  margin: 20px 0;
  padding: 10px;
  padding-right: 80px;

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
`;

function getFileName(path) {
  const parts = path.split("/");
  return parts[parts.length - 1];
}

function ResultPanel({result}) {
  return (
    <Container>
      <div>{result.text}</div>
      <SourceLink href={result.file_path} target='_blank'>{getFileName(result.file_path)}</SourceLink>
      <div className="score-value">{result.score}</div>
    </Container>
  );
}

export default ResultPanel;
