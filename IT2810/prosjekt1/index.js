(() => {

    const canvas = document.querySelector("#daVinky")

    canvas.width  = window.innerWidth/2
    canvas.height = window.innerHeight/2
    


    const ctx = canvas.getContext("2d")


    function makeCircle(x,y,r,color){      
        ctx.beginPath()
        ctx.arc(x, y, r, 0, 2*Math.PI)
        ctx.fillStyle = color
        ctx.fill()
    }
    

    function draw(){

        
    ctx.fillStyle = "tomato"
    ctx.fillRect(10, 20, 200, 300)

    //head
    makeCircle(190, 245, 60,"green"), ctx.stroke();
    makeCircle(110, 245, 60,"green"), ctx.stroke();
    makeCircle(120, 345, 120,"green");

    //eyes
    makeCircle(230, 245, 30,"white"), ctx.stroke();
    makeCircle(150, 245, 30,"white"), ctx.stroke();

    makeCircle(150, 245, 15,"black");
    makeCircle(230, 245, 15,"black");

    //makeCircle(155, 250, 5,"white");
    //makeCircle(235, 250, 5,"white");

    //mouth
    ctx.beginPath();
    ctx.moveTo(90, 320);
    ctx.lineTo(120, 340);
    ctx.lineTo(150, 355);
    ctx.lineTo(180, 360);
    ctx.lineTo(200, 361);
    ctx.lineTo(220, 355);
    ctx.lineTo(240, 345);
    ctx.lineTo(250, 330);
    ctx.fillStyle = "red";
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(250, 330);
    ctx.lineTo(240, 315);
    ctx.lineTo(220, 305);
    ctx.lineTo(200, 299);
    ctx.lineTo(180, 300);
    ctx.lineTo(150, 305);
    ctx.lineTo(120, 320);
    ctx.lineTo(90, 330);
    ctx.fillStyle = "red";
    ctx.fill();

    //shirt
    ctx.beginPath();
    ctx.moveTo(15, 400);
    ctx.lineTo(30, 410);
    ctx.lineTo(50, 415);
    ctx.lineTo(75, 420);
    ctx.lineTo(100, 421);
    ctx.lineTo(125, 420);
    ctx.lineTo(150, 418);
    ctx.lineTo(170, 416);
    ctx.lineTo(190, 425);
    ctx.lineTo(205, canvas.height);
    ctx.lineTo(0, canvas.height);
    ctx.fillStyle = "blue";
    ctx.fill();
}

let x = 236;
let y = 156;
let baseX = 237;
let baseY = 157;
var color = "white" 
function render() {
  ctx.clearRect(0,0,canvas.width,canvas.height);
  let deltaX = -0.4;
  let deltaY = 0.3;
  x += deltaX;
  y += deltaY;
  draw();
  console.log(x);
    
  ctx.beginPath()
  ctx.arc(x, 245+((baseX-x)*1.5), 5, 0, (2)*Math.PI)
  ctx.fillStyle = color
  ctx.fill()

  ctx.beginPath()
  ctx.arc(y, 245+(baseY-y)*2, 5, 0, (2)*Math.PI)
  ctx.fillStyle = color
  ctx.fill()
  requestAnimationFrame(render);
    if(x<230){
        x=233;
    }

    if(y>153){
        y=150;
    }
}
render();

  })()