function update_href(query) {
  query = new Map(Object.entries(query));
  const url = new URL(window.location.href);
  const params = new URLSearchParams(url.search);
  for (const [key, value] of query) {
    params.set(key, value);
  }
  url.search = params.toString();
  window.location.href = url.href;
}
