//-------全局---------------

var tags = [];
var tag_article = {};

//-------------------------
function show(text){
    if(text == 'index'){
        $('.line').css('opacity', '0');
        $('.line-1').css('opacity', '1');
        $('.line-1-b').css('opacity', '1');
        $('.body-main').css('display', 'none');
        $('.pack-up').css('display', 'block');
        $('.index').css('display', 'block');
        window_index_article();
    }
    if(text == 'tags'){
        $('.line').css('opacity', '0');
        $('.line-2').css('opacity', '1');
        $('.line-2-b').css('opacity', '1');
        $('.body-main').css('display', 'none');
        $('.pack-up').css('display', 'block');
        $('.tags').css('display', 'block');
    }
    if(text == 'other'){
        $('.line').css('opacity', '0');
        $('.line-3').css('opacity', '1');
        $('.line-3-b').css('opacity', '1');
        $('.body-main').css('display', 'none');
        $('.pack-up').css('display', 'block');
        $('.other').css('display', 'block');
    }
}

function pack(){
    $('.line').css('opacity', '0');
    $('.pack-up').css('display', 'none');
    $('.body-main').css('display', 'none');
}

function view(t){
    var tag = $(t).attr('name');
    var title = $(t).attr('id');
    $.ajax({url:'/get-article-api/', type:'POST', data:{'tag': tag, 'title': title}, success:function(d){
        if(d != 'failed'){
            edit_content();
            $('.menu-tag-select').val(tag);
            $('.menu-title-input').val(title);
            $('.edit-panel-text').val(d);
            render();
        }
    }})
}

function window_tag_article(id, ta){
    $('.content-panel').children().remove();
    for(var i=0; i<ta.length; i++){
        var article_tip = "<div class='article-tip'"+" id='"+ta[i][0]+"' onclick='view(this)'"
            +" name='"+id+"'"+">"+"<span class='article-tip-s1'>"+ta[i][0]
            +"</span>"+"<span class='article-tip-s2'>"+ta[i][1]+"</span>"+"</div>";
        $('.content-panel').prepend($(article_tip));
    }
}

function window_index_article(){
    $('.index').children().remove();
    for(var i = 0; i < window.tags.length; i++){
        for(var j = 0; j < window.tag_article[window.tags[i]].length; j++){
            var url = "/index-get-article/?tag="+window.tags[i]+"&title="+window.tag_article[window.tags[i]][j][0];
            var index_div = "<div align='center' onclick=show_article("+"'"+url+"'"+") class='index-div'"+">"+"<h2>"
                +window.tag_article[window.tags[i]][j][0]+"</h2></div>";
            $('.index').append($(index_div));
        }
    }
}

function show_article(url){
    $.ajax({url:url, type:'GET', data:{}, success:function(d){
        $('.index-article').css('display', 'block');
        $('.append-text').children().remove();
        var convert = new showdown.Converter();
        var html = convert.makeHtml(d);
        $('.append-text').append($(html));
    }});
}

function tag_o(id){
    select = '#'+id;
    $('.tag-div').css('background', '#331');
    $(select).css('background', '#cf0');
    var t_a = window.tag_article[id];
    window_tag_article(id, t_a);
}

function add_tag(){
    $('.add-tag-frame').css('display', 'block');
}

function delete_tag(id){
    $('.delete-tag').css('display', 'block');
    $('.delete-tag-info').text('删除标签<'+id+'>');
    $('.delete-tag').attr('did', id);
}

function over(cls){
    $(cls).css('background', '#cf0');
}

function delete_tag_cancel(){
    $('.delete-tag').css('display', 'none');
    $('.delete-tag-info').text('');
}

function delete_tag_confirm(){
    var deleting_tag = $('.delete-tag').attr('did');
    $.ajax({url:'/delete-tag-api/', type:'POST', data:{'deleting_tag': deleting_tag}, success:function(d){
        if(d == 'done'){
            $('.delete-tag').css('display', 'none');
            window.tags.splice(window.tags.indexOf(deleting_tag), 1);
            var id = '#'+deleting_tag;
            $(id).remove();
        }
        else{
            $('.delete-tag').css('display', 'none');
        }
    }})
}

function leave(cls){
    $(cls).css('background', '#132');
}

function windows_tags(){
    for(var i = 0; i < window.tags.length; i++){
        var tmp = "'"+window.tags[i]+"'";
        var tag_div = "<div class='tag-div' onclick=delete_tag("+tmp+")"+" onmouseover=tag_o("+tmp+")"
            +" id="+tmp+">"+window.tags[i]+"</div>";
        $('.tags-panel').prepend($(tag_div));
    }
}

function add_tag_confirm(){
    var new_tag = $('.add-tag-frame-input').val();
    if(new_tag){
        $('.add-tag-frame').css('display', 'none');
        $.ajax({url:'/add-tag-api/', type:'POST', data:{'new_tag': new_tag}, success:function(d){
            if(d == 'done'){
                window.tags.push(new_tag);
                var tmp = "'"+new_tag+"'";
                var tag_div = "<div class='tag-div' onclick=delete_tag("+tmp+")"+"onmouseover=tag_o("
                    +tmp+")"+" id="+tmp+">"+new_tag+"</div>";
                $('.tags-panel').prepend($(tag_div));
            }
        }})
    }
    $('.add-tag-frame').css('display', 'none');
}

function edit_content(){
    $('.edit-panel').css('display', 'block');
    $('.edit-panel-render').children().remove();
    $('.edit-panel-render').text('');
    $('.edit-panel-text').val('');
    $('.menu-title-input').val('');
    $('.menu-title-input').attr('placeholder', 'The title?');
    $('.menu-tag-select').children().remove();
    for(var i = 0; i < window.tags.length; i++){
        var tmp = "<option "+"value='"+window.tags[i]+"'"+">"+window.tags[i]+"</option>";
        $('.menu-tag-select').append($(tmp));
    }
}

function edit_panel_none(){
    $('.edit-panel').css('display', 'none');
    $('.index-article').css('display', 'none');
}

function render(){
    var text = $('.edit-panel-text').val();
    $('.edit-panel-render').children().remove();
    var convert = new showdown.Converter();
    var html = convert.makeHtml(text);
    $('.edit-panel-render').append($(html));
}

function edit_submit(){
    var title = $('.menu-title-input').val();
    var bode = $('.edit-panel-text').val();
    var tag = $('.menu-tag-select').val();
    if(title == ''){
        $('.menu-title-input').attr('placeholder', 'title不能为空 :)');
        return;
    }
    else if(bode == ''){
        return;
    }
    else{
        $('.edit-submit-confirm').css('display', 'block');
        var tip = "["+tag+"]"+"标签下"+"<"+title+">"+"文章将被修改";
        $(".edit-submit-confirm-tip").text(tip);
    }
}

function edit_submit_no(){
    $('.edit-submit-confirm').css('display', 'none');
}

function new_article(tag, title){
    for(var i = 0; i < window.tag_article[tag].length; i++){
        if(window.tag_article[tag][i][0] == title){
            window.tag_article[tag].splice(i, 1);
            return 0;
        }
    }
    return 1;
}

function edit_submit_yes(){
    $('.edit-submit-confirm').css('display', 'none');
    var title = $('.menu-title-input').val();
    var bode = $('.edit-panel-text').val();
    var tag = $('.menu-tag-select').val();
    $.ajax({url:'/add-article-api/', type:'POST', data:{'tag': tag, 'title': title, 'bode': bode}, success:function(d){
        if(d == 'done'){
            if(new_article(tag, title)){
                window.tag_article[tag].push([title, '新添加']);
                edit_panel_none();
            }
            else{
                window.tag_article[tag].push([title, '新修改']);
                edit_panel_none();
            }
        }
    }})
}

$(function(){
    $.ajax({url:'/get-tags-api/', type:'POST', data:{}, success:function(d){
        window.tags = eval(d);
        windows_tags();
    }})
    $.ajax({url:'/get-tag-article-api/', type:'POST', data:{}, success:function(d){
        window.tag_article = eval("("+d+")");
        window_index_article();
    }})
})
