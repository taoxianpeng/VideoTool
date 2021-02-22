// $(".item-btn").click(play);
'use-strict'
// 字符串格式化方法
String.prototype.format = function(){
    if(arguments.length==0){
      return this;
    }
    for(var s=this, i=0; i<arguments.length; i++){
      s = s.replace(new RegExp("\\{"+i+"\\}","g"), arguments[i]);
    }
    return s;
  };

function parse(){
    let url = $("#search-input").val();
    if(url==""){
        window.alert("请输入解析的网页地址！");
        return;
    }
    $.ajax({
        type:"get",
        dataType:"json",
        data:{'url':url},
        url:"./getItemList",
        success:(jsons)=>{
            $(".item-btn").remove();
            let index=1;
            for(item in jsons){
                var tempBtn = '<button class="item-btn" title="{0}" src="{1}" onclick="play(this)">{2}</button>';
                $(".item-group").append(tempBtn.format(item,jsons[item],index));
                index+=1;
            }
            // $(".item-group").append("");
         
        },
        error:(msg)=>{
            $(".item-btn").remove();
            let enj = $("#jk").find("option:selected").attr('value');
            $(".player").attr('src',enj+url);
        }
        
    })
};

function play(obj){
    $(obj).css("background-color","#1e1e36")
    $(obj).css("color","#ff5c38")
    let enj = $("#jk").find("option:selected").attr('value');
    // let url = "https://www.playm3u8.cn/jiexi.php?url="+$(obj).attr('src')
    let url = enj+$(obj).attr('src');
    $(".player").attr('src',url);
}
