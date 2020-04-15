d3.select("#book-list").html('');

var url_list="/api/bookList";
d3.json(url_list, function(response){

    console.log(response);
    

    const bookList= book=> `<div class="book-item">
                                <div class="row">
                                    <div class="col-lg-4">
                                        <div class="book-info-box">
                                            <img src="${book.image_url}" alt="">
                                            <div class="book-info">
                                                <h4 id='title'>${book.title}</h4>
                                                <p>${book.author}</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-lg-6">
                                        <div class="single_player_container">
                                            <div class="row">
                                                <div class="col-sm-3">
                                                    <h6>Genre</h6>
                                                    <p>${book.sub_category}</p>
                                                </div>
                                                <div class="col-sm-3">
                                                    <h6>Rating</h6>
                                                    <p>${book.average_rating}</p>
                                                </div>
                                                <div class="col-sm-3">
                                                    <h6>No. of Pages</h6>
                                                    <p>${book.num_pages}</p>
                                                </div>
                                                <div class="col-sm-3" style="display:none;">
                                                    <h6>ISBN</h6>
                                                    <p id="isbn">${book.isbn}</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-lg-2">
                                        <div class="books-links">
                                            <a href=""><img src="../static/img/icons/p-1.png" alt=""></a>
                                            <a id="share"><img src="../static/img/icons/p-2.png" alt=""></a>
                                            <a href="/bookSearch"><img src="../static/img/icons/p-3.png" alt=""></a>
                                        </div>
                                    </div>
                                </div>
                            </div>`


    document.querySelector("#book-list")
    .innerHTML = response.map(book => bookList(book)).join('');

    d3.selectAll(".book-item").on("click", function() {
    
       title = d3.select(this).select("#title").text()
       isbn=d3.select(this).select("#isbn").text()
       d3.select(this).select("#share").attr("href",`/getuserinputs/${isbn}`)
       console.log(title)
       console.log(isbn)

       });
       
    
});

