export async function search(query) {
  const resp = await fetch(`/api/search?query=${query}`);
  return (await resp.json())["results"];
}
