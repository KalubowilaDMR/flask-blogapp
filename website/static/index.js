// function like(postId){
//     console.log('clicks', postId);
// }
const like = (postId) => {
    const count = document.getElementById(`like-count-${postId}`)
    const button = document.getElementById(`like-button-${postId}`)

    url = `/like/${postId}`

    fetch(url, {method : 'POST'})
    .then((res) => res.json())
    .then((data) => {
        count.innerHTML = data['likes']
        if(data['liked'] === true){
            button.className = "bi bi-hand-thumbs-up-fill"
        } else {
            button.className = "bi bi-hand-thumbs-up"
        }
    });
}


