/**
 * Скрипт получает все видосы из "танцевальное по лайту":
 * https://www.youtube.com/playlist?list=PLdb8DVmvU9i5bGINNz10f-ga_bqD41O4q
 * 
 * Затем перемешивает их в случайном порядке.
 * 
 * Для запуска скрипта нужно добавить YouTube Data API v3 в Services
 * 
 * https://developers.google.com/youtube/v3/quickstart/apps-script?hl=en
 * https://developers.google.com/youtube/v3/docs/playlistItems/update?hl=en
 */
function main() {
  // Получаем все видосы
  playlistId = "PLdb8DVmvU9i5bGINNz10f-ga_bqD41O4q"
  maxResults = 50
  pageToken = null 
  allItems = [];
  while (true) {
    resp = YouTube.PlaylistItems.list("snippet", {playlistId, maxResults, pageToken});
    allItems = [...allItems, ...resp.items];
    if (resp.items.length < maxResults) {
      break;
    }
    else {
      pageToken = resp.nextPageToken;
    }
  } 

  // Мешаем видосы
  shuffle(allItems);
  allItems.forEach((plItem, index) => {
    console.log(`${index + 1} / ${allItems.length}`);
    YouTube.PlaylistItems.update(
      {
        id: plItem.id,
        snippet: {
          playlistId: plItem.snippet.playlistId,
          position: Math.floor(Math.random() * allItems.length),
          resourceId: plItem.snippet.resourceId,
        }
      }, 
      ["snippet"]
    );
  });
}

/**
 * Перемешивает массив
 * https://stackoverflow.com/a/2450976/5500609
 */
function shuffle(array) {
  var currentIndex = array.length,  randomIndex;

  // While there remain elements to shuffle...
  while (currentIndex != 0) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    // And swap it with the current element.
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex], array[currentIndex]];
  }

  return array;
}