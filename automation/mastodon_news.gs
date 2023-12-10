function myFunction() {
  const newsApiKey = '*******************************';
  const mastodonKey = '*******************************';

  const sources = ['bbc-news', 'cnn', 'the-verge', 'time', 'the-wall-street-journal'];
  const source = sources[Math.floor(Math.random() * sources.length)];

  Logger.log('\n' + source);

  const newsApiUrl = `https://newsapi.org/v1/articles?source=${source}&sortBy=top&apiKey=${newsApiKey}`;
  const response = UrlFetchApp.fetch(newsApiUrl);
  const articles = JSON.parse(response.getContentText()).articles;

  for (const article of articles) {
    if (!article.description) {
      article.description = 'Read More';
    }

    const tweet = `➡️ ${article.title}\n\n${article.description}\n\n${article.url}`;

    const mastodonUrl = 'https://mastodon.social/api/v1/statuses';
    const authHeaders = {
      'Authorization': `Bearer ${mastodonKey}`
    };

    const params = { 'status': tweet };

    const options = {
      method: 'post',
      headers: authHeaders,
      payload: params
    };

    const mastodonResponse = UrlFetchApp.fetch(mastodonUrl, options);
    const mastodonRes = JSON.parse(mastodonResponse.getContentText());
    Logger.log('\n' + mastodonRes.url);
  }
}
