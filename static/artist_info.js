
function getBio(artist){
  var current_artist = document.querySelector('.bio');
  current_artist.innerHTML = artist;
  console.log(current_artist)
}

function getPic(artist){
  var current_artist_pic = document.querySelector('.currentpic');
  current_artist_pic.src = artist;
  console.log(current_artist_pic.src)

}
