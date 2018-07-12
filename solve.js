var buttons = document.getElementsByClassName("_3e_exnkhzU1IzEtnY-Il71");
var resetButton = document.getElementsByClassName("_1bxrRV1ZhB4iF88UCCptiW");

var moveUp    = () => { buttons[0].click(); };
var moveDown  = () => { buttons[3].click(); };
var moveLeft  = () => { buttons[1].click(); };
var moveRight = () => { buttons[2].click(); };
var reset     = () => { resetButton[0].click(); };

var findReactComponent = function(el) {
  for (const key in el) {
    if (key.startsWith('__reactInternalInstance$')) {
      const fiberNode = el[key];

      return fiberNode && fiberNode.return && fiberNode.return.stateNode;
    }
  }
  return null;
};

var alert = (message) => { console.log(message); };

var root = findReactComponent(document.getElementById("root").firstChild);

var SIZE = 150

var getAdjList  = ()        => { return root.state.adjList; };
var getCoord    = ()        => { return {"x": root.state.curCol, "y": root.state.curRow}; };
var coord2index = (coord)   => { return SIZE * coord["y"] + coord["x"]; };
var index2coord = (index)   => {
    var rem = index % SIZE;
    var quotient = Math.floor(index / SIZE);
    return {"x": rem, "y": quotient};  
};

function bfs(start_coord, end_coord)
{
    var start_index = coord2index(start_coord);
    var end_index = coord2index(end_coord);
    var adjList = getAdjList();

    var queue = [start_index];
    var visited = [];
    var n = SIZE * SIZE;
    for (var i = 0; i < n; i++)
    {
        visited.push([false, []]);
    }
    visited[start_index] = [true, [start_index]];

    while (queue.length > 0)
    {
        if (queue.indexOf(end_index) != -1)
        {
            return [true, visited[end_index][1]];
        }

        var tempQueue = [];
        for (var position in queue)
        {
            position = queue[position];
            var __tempQueue = adjList[position];

            _tempQueue = [];
            for (var temp in __tempQueue)
            {
                temp = __tempQueue[temp];
                if (!visited[temp][0])
                {
                    _tempQueue.push(temp);
                }
            }

            for (var nextPosition in _tempQueue)
            {
                nextPosition = _tempQueue[nextPosition];
                visited[nextPosition][0] = true;
                visited[nextPosition][1] = visited[position][1].concat([nextPosition]);
            }

            tempQueue = tempQueue.concat(_tempQueue);
        }

        queue = tempQueue;
    }

    return [false, []];
}

function moveTowards(targetCoord)
{
    var startCoord = getCoord();
    console.log("(" + startCoord["x"] + ", " + startCoord["y"] + ")")
    var end_index = coord2index(targetCoord);
    var start_index = coord2index(startCoord);

    if (start_index == end_index)
    {
        console.log("Already there");
        return 1;
    }

    var dfsSolution =  bfs(startCoord, targetCoord);
    var possible = dfsSolution[0], path = dfsSolution[1];

    if (!possible)
    {
        console.log("Not possible");
        return -1;
    }

    var first = index2coord(path[0]);
    var second = index2coord(path[1]);

    var delta_x = second["x"] - first["x"];
    var delta_y = second["y"] - first["y"];

    if (delta_x == 1)
    {
        moveRight();
    }
    else if (delta_x == -1)
    {
        moveLeft();
    }
    else if (delta_y == 1)
    {
        moveDown();
    }
    else if (delta_y == -1)
    {
        moveUp();
    }
    else
    {
        return -1;
    }
    return 0;
}

function moveTo(coord, callback = (() => {}))
{
    var resultID = moveTowards(coord);
    if (resultID == -1)
    {
        console.log("Stopped moving");
        callback(false);
    }
    else if (resultID == 1)
    {
        console.log("Successfully moved");
        callback(true);
    }
    else if (resultID == 0)
    {
        setTimeout(() => { moveTo(coord, callback); }, 50);
    }
}

function tryMove(coord, tries = 5)
{

    if (tries <= 0)
    {
        return;
    }
    var callback = (succ) => {
        if (succ)
        {
            console.log("DONE TRYING");
        }
        else
        {
            reset();
            setTimeout(() => { tryMove(coord, tries - 1); }, 500);
        }
    };
    console.log("Trying to move to " + coord + "; " + tries + " tries left");
    moveTo(coord, callback);
}
