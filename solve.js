buttons = document.getElementsByClassName("_3e_exnkhzU1IzEtnY-Il71");
resetButton = document.getElementsByClassName("_1bxrRV1ZhB4iF88UCCptiW");

// keep track of current position
var current_x = 0, current_y = 0;
var tiles = {};
console.log("RELOAD");

var moveUp    = () => { buttons[0].click(); return [current_x, current_y - 1]; };
var moveDown  = () => { buttons[3].click(); return [current_x, current_y + 1]; };
var moveLeft  = () => { buttons[1].click(); return [current_x - 1, current_y]; };
var moveRight = () => { buttons[2].click(); return [current_x + 1, current_y]; };
var reset     = () => { console.log("RESET"); resetButton[0].click(); current_x = 0; current_y = 0; tiles = {}; };
var running = true;

var stuckMesg = "You are stuck, go ahead and reset!";

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// alert handler to detect bad moves
var alertHappened = false;
var alertMesg = "";
// overwrite default alert function so popup doesn't happen
var alert = (message) => { 
    if (message == stuckMesg)
    {
        running = false;
    }
    else 
    {
        alertHappened = true;
        alertMesg = message;
    }
};
// check if alert happens after running function f
async function checkAlert(cb, f)
{
    var args = Array.prototype.splice.call(arguments, 2);
    alertHappened = false;
    var result = f.apply(null, args);
    await sleep(200);
    if (!running)
    {
        console.log("FORCE STOP");
        return;
    }
    var finalResult = {
        "alert": alertHappened, 
        "mesg": alertMesg, 
        "return": result
    };
    cb(finalResult);
};

var randInt = (min, max) => { return Math.floor(Math.random() * (max - min + 1)) + min; };

var moveOptions = [moveDown, moveRight, moveUp, moveLeft];

var hashCoord = (x, y) => { return x + ":" + y };

async function explore(totalMoves = 10, newMove = 0)
{
    if (totalMoves == 0)
    {
        console.log("DONE EXPLORING");
        return;
    }

    var index = hashCoord(current_x, current_y);

    var callback = (mode) => {
        var _function = (result) => {
            var moved = false;

            // check if validly moved
            if (!result["alert"])
            {
                moved = true;
                tiles[index]["dir"][dirIndex][1] += 1;

                // update x and y coordinates
                current_x = result["return"][0];
                current_y = result["return"][1];
                console.log(current_x + ", " + current_y)
            }
            tiles[index]["dir"][dirIndex][0] = !result["alert"];

            if (moved)
            {
                explore(totalMoves - 1);
            }
            else
            {
                explore(totalMoves, newMove = mode);
            }
        }
        return _function;
    };

    if ((newMove == 0 && index in tiles) || newMove == 2) // if visited before
    {
        var tile = tiles[index];

        // increment count of number of times visited this tile
        if (newMove == 0)
        {
            tile["count"] += 1;
        }

        var dirIndex = -1;
        var minVisits = 9999;
        // find direction least explored
        for (var i = 0; i < tile["dir"].length; i++)
        {
            var moveOption = tile["dir"][i];
            if (moveOption[0] !== false && moveOption[1] < minVisits)
            {
                dirIndex = i;
                minVisits = moveOption[1];
            }
        }

        // try to move in that direction
        checkAlert(callback(2), moveOptions[dirIndex]);
    }
    else
    {
        tiles[index] = {"dir": [[null, 0], [null, 0], [null, 0], [null, 0]], "count": 1};
        var moved = false;
        
        // choose random direction to move in
        var dirIndex = randInt(0, moveOptions.length - 1) % 4;

        // try to move in that direction 
        checkAlert(callback(1), moveOptions[dirIndex]);
    }
}

var moveOptions = [moveDown, moveRight, moveDown, moveRight, moveUp, moveLeft];
var xxxxx = 100;
for (var i = 0; i < xxxxx; i++)
{
    if (!running)
    {
        break;
    }
    var x = randInt(0, moveOptions.length - 1);
    var move = moveOptions[x];
    move(); 
}