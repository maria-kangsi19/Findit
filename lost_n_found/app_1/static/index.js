
function showOnly(stateClass) {
   
    document.querySelectorAll('.card').forEach(card => {
        card.style.display = 'none';
    });

    
    document.querySelectorAll('.' + stateClass).forEach(card => {
        card.style.display = 'block';
    });
}
function showAll() {
  
    document.querySelectorAll('.card').forEach(card => {
        card.style.display = 'block';
    });
}
async function loadPosts() {
    const response = await fetch("http://127.0.0.1:8000/api/posts/");
    const posts = await response.json();

    const container = document.getElementById("post-container");
    container.innerHTML = "";

    posts.forEach(post => {
        const div = document.createElement("div");
        div.classList.add("card", "p-3", "m-3");

        div.innerHTML = `
            <h4>${post.post_type.toUpperCase()}</h4>
            <p>${post.description}</p>
            <p><b>Reward:</b> ₹${post.reward || "0"}</p>
        `;

        container.appendChild(div);
    });
}


loadPosts();
