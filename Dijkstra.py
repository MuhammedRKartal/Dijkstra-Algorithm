from collections import defaultdict
import heapq
import math
import tkinter as tk
import time
import tkinter.messagebox


N = 0
source = 0
destination = 0

def click_button():

    myCanvas.delete("all")

    #Make sure that user selects Graph size, source and destination
    try: N = int(N_entry.get())
    except(Exception): N = "Enter N"
    try: source = int(S_entry.get())
    except(Exception): source = "Enter S"
    try: destination = int(D_entry.get())
    except(Exception): destination = "Enter D"
    if (N == 'Enter N' or (N<3 or N>20)):
        tk.messagebox.showwarning("Warning","Please select N between 3 and 20")
    elif (source == "Enter S" or source>N-1):
        tk.messagebox.showwarning("Warning", "Please select a Src between 0 and " + str(N-1))
    elif (destination == "Enter D" or destination>N-1 ) :
        tk.messagebox.showwarning("Warning", "Please select a Dest between 0 and " + str(N-1))

    #After all selections start operations
    else:

        edges = create_edges(N) #create edges between verticies

        #calculate running time of algorithm
        starttime = time.perf_counter()
        weight, path = dijkstra(edges, source, destination)
        totaltime = "Runtime "+  " - "+str(int((time.perf_counter() - starttime)*1000000)) + " milliseconds"


        #Place the texts on GUI.
        myCanvas.create_text(xSize / 2, ySize / 10, fill="darkblue", font="Times 40 bold",
                             text="Djikstra Algorithm")

        myCanvas.create_text(xSize / 2, int(ySize / 5) * 3, fill="black", font="Times 25 ",
                             text="[S] " + str(source) + " → " + str(destination) + " [D]")

        myCanvas.create_text(xSize / 2, int(ySize / 5) * 3.35, fill="black", font="Times 25 ",
                             text="W = " + str(weight))

        for p in range(1, len(path)):
            myCanvas.create_text((xSize / 2) * (p / 7), int(ySize / 5) * 3.60, fill="black", font="Times 25 ",
                                 text=str(path[p - 1]) + "→")
        myCanvas.create_text((xSize / 2) * (len(path) / 7), int(ySize / 5) * 3.60, fill="black", font="Times 25 ",
                        text=str(path[len(path)-1]))

        #calculate basic features to place elements on optimal positions on different scales.
        uY, uArr, dY, dArr = calculate_position(xSize, ySize, N)

        #Create Verticies
        for i in range(len(uArr)):
            create_circle(uArr[i], uY, 20, myCanvas)
            myCanvas.create_text(uArr[i], uY, fill="darkblue", font="Times 20",
                                 text=2 * i)
        for i in range(len(dArr)):
            create_circle(dArr[i], dY, 20, myCanvas)
            myCanvas.create_text(dArr[i], dY, fill="darkblue", font="Times 20",
                                 text=str(2 * i + 1))
            #Create edges between down side verticies.
            if (i != len(dArr) - 1):
                myCanvas.create_line(dArr[i] + 20, dY, dArr[i + 1] - 20, dY, width=2)

        #Create cross,up and down edges
        if (N % 2 == 0):
            for i in range(len(uArr)):
                if (i != len(uArr) - 1):
                    myCanvas.create_line(uArr[i] + 20, uY, uArr[i + 1] - 20, uY, width=2)
                    if (N % 2 == 0):
                        myCanvas.create_line(uArr[i], uY + 20, uArr[i + 1], dY - 20, width=2)
                        myCanvas.create_line(uArr[i + 1], uY + 20, uArr[i], dY - 20, width=2)
                    else:
                        pass
                myCanvas.create_line(uArr[i], uY + 20, uArr[i], dY - 20, width=2)
        else:
            for i in range(len(dArr)):
                a = len(dArr) - 1
                if (i == a):
                    myCanvas.create_line(dArr[i], dY - 20, uArr[i + 1], uY + 20, width=2)
                    myCanvas.create_line(uArr[i] + 20, uY, uArr[i + 1] - 20, uY, width=2)

                if (i != len(dArr) - 1):
                    myCanvas.create_line(dArr[i] + 20, uY, dArr[i + 1] - 20, uY, width=2)
                    if (N % 2 == 1):
                        myCanvas.create_line(dArr[i], uY + 20, dArr[i + 1], dY - 20, width=2)
                        myCanvas.create_line(dArr[i + 1], uY + 20, dArr[i], dY - 20, width=2)
                    else:
                        pass
                myCanvas.create_line(dArr[i], uY + 20, dArr[i], dY - 20, width=2)
        myCanvas.pack()

        i = 0
        while (i != len(path)):
            if (i != len(path) - 1):
                if ((path[i] % 2 == 0 and path[i + 1] % 2 == 0)):
                    if (path[i] > path[i + 1]):
                        x = -20
                    else:
                        x = 20
                    myCanvas.create_line(uArr[int(path[i] / 2)] + x, uY, uArr[int(path[i + 1] / 2)] - x, uY, fill="red",
                                         width=8)

                elif (path[i] % 2 == 1 and path[i + 1] % 2 == 1):
                    if (path[i] > path[i + 1]):
                        x = -20
                    else:
                        x = 20
                    myCanvas.create_line(dArr[int(path[i] / 2)] + x, dY, dArr[int(path[i + 1] / 2)] - x, dY, fill="red",
                                         width=8)

                elif (path[i] % 2 == 1 and path[i + 1] % 2 == 0):
                    myCanvas.create_line(dArr[int(path[i] / 2)], dY - 20, uArr[int(path[i + 1] / 2)], uY + 20, fill="red",
                                         width=8)

                elif (path[i] % 2 == 0 and path[i + 1] % 2 == 1):
                    myCanvas.create_line(uArr[int(path[i] / 2)], uY + 20, dArr[int(path[i + 1] / 2)], dY - 20, fill="red",
                                         width=8)

            myCanvas.update()
            time.sleep(1)
            i += 1

        #Print time into GUI
        myCanvas.create_text((xSize / 2), int(ySize / 5) * 4, fill="black", font="Times 25 ",
                             text=str(totaltime))
        myCanvas.update()

def create_circle(x, y, r, canvasName):  # center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1,width = 2)

#That method calculates optimal positions for given scales and graph size
def calculate_position(scX,scY,N):
    U=math.ceil(N/2)
    D=N-U
    UK=(scX/U)*1.75

    uArr=[]
    dArr=[]
    UY=math.ceil((scY/5)*1.30)
    DY=math.ceil((scY/5)*2.5)
    for i in range(1,U+1):
        uArr.append(UK*(i/2))
    for i in range(1,D+1):
        dArr.append(UK*(i/2))
    return UY,uArr,DY,dArr

#Create edges between veriticies on given formula W(i,j) = i+j
def create_edges(N):
    edges = list()
    edges.append((0, 1, 1))
    edges.append((0, 2, 2))
    edges.append((0, 3, 3))
    edges.append((1, 0, 1))
    edges.append((1, 2, 3))
    edges.append((1, 3, 4))

    if (N % 2 == 0):
        for i in range(2, N, 2):
            if (i == N - 2):
                edges.append((i, i - 1, 2*i-1))
                edges.append((i, i - 2, 2*i-2))
                edges.append((i, i + 1, 2*i+1))
            else:
                edges.append((i, i - 1, 2*i-1))
                edges.append((i, i - 2, 2*i-2))
                edges.append((i, i + 1, 2*i+1))
                edges.append((i, i + 2, 2*i+2))
                edges.append((i, i + 3, 2*i+3))
        for i in range(3, N, 2):
            if (i == N - 1):
                edges.append((i, i - 1, 2*i-1))
                edges.append((i, i - 2, 2*i-2))
                edges.append((i, i - 3, 2*i-3))
            else:
                edges.append((i, i - 1, 2*i-1))
                edges.append((i, i - 2, 2*i-2))
                edges.append((i, i + 1, 2*i+1))
                edges.append((i, i + 2, 2*i+2))
                edges.append((i, i - 3, 2*i-3))

    else:
        for i in range(2, N, 2):
            if (i == N - 1):
                edges.append((i, i - 1, 2*i-1))
                edges.append((i, i - 2, 2*i-2))
            elif (i == N - 3):
                edges.append((i, i - 1, 2*i-1))
                edges.append((i, i - 2, 2*i-2))
                edges.append((i, i + 1, 2*i+1))
                edges.append((i, i + 2, 2*i+2))
            else:
                edges.append((i, i - 1, 2*i-1))
                edges.append((i, i - 2, 2*i-2))
                edges.append((i, i + 1, 2*i+1))
                edges.append((i, i + 2, 2*i+2))
                edges.append((i, i + 3, 2*i+3))
        for i in range(3, N, 2):
            if (i == N - 2):
                edges.append((i, i - 1, 2*i-1))
                edges.append((i, i - 2, 2*i-2))
                edges.append((i, i - 3, 2*i-3))
                edges.append((i, i + 1, 2*i+1))
            else:
                edges.append((i, i - 1, 2*i-1))
                edges.append((i, i - 2, 2*i-2))
                edges.append((i, i + 1, 2*i+1))
                edges.append((i, i + 2, 2*i+2))
                edges.append((i, i - 3, 2*i-3))
    return edges



def dijkstra(edges, source, destination):
    #Fill graph
    # DefaultDict helps for ex: add dict sth if its null add null
    graph = defaultdict(list)

    #each column of graph holds weight and destination vertex
    for src,dst,weight in edges:
        graph[src].append((weight,dst))

    #heap is a list of tuples
    #seen is a set which has unique seen elements
    #weights is a dictionary that holds weight of each source
    heap, seen, weights = [(0, source,())], set(), {source: 0}

    while heap:
        ####Create optimal path####
        #totalweight is integer value
        #currSrc is a random value
        #path is a tuple of size n
        (totalWeight,currSrc,path) = heapq.heappop(heap)
        if currSrc in seen: continue
        seen.add(currSrc)
        path += (currSrc,) #add new source to path

        if currSrc == destination: return totalWeight, path

        #Fill the weights of whole graph
        for weight, currDst in graph.get(currSrc, ()):
            if currDst in seen: continue
            prev = weights.get(currDst,None)
            next = totalWeight + weight
            if prev == None or next < prev:
                weights[currDst] = next
                heapq.heappush(heap, (next, currDst, path))

    return 99999999,()

if __name__ == "__main__":

    #Create a window for GUI.
    root = tk.Tk()
    xSize, ySize = 900,600
    size = str(xSize) + "x" + str(ySize)
    root.geometry(size)
    root.resizable(False,False)
    root.title("Djikstra Algorithm")
    root.configure(bg='darkred')

    #Create canvas to create different graphs and visualize
    myCanvas = tk.Canvas(root)
    myCanvas.config(width=xSize, height=ySize,bg='white')

    #Input from user
    entryText1 = tk.StringVar()
    N_entry = tk.Entry(root,textvariable=entryText1)
    entryText1.set("Enter N")
    N_entry.pack(anchor = "w")

    entryText2 = tk.StringVar()
    S_entry = tk.Entry(root,textvariable=entryText2)
    entryText2.set("Enter Src")
    S_entry.pack()

    entryText3 = tk.StringVar()
    D_entry = tk.Entry(root,textvariable=entryText3)
    entryText3.set("Enter Dest")
    D_entry.pack(anchor = "e")

    #Button to run Djikstra with given values
    button_N = tk.Button(root, text="Enter N,S,D", command=click_button)
    button_N.pack()

    root.mainloop()


    ###############################Tests and Graph Visualisation##################################
    # tests = []
    # for i in range (0,2010,100):
    #     tests.append(i)


    # tests = [10,50,100,200,500,1000,2000]
    # test_array = []
    # times_array = []
    #
    # time_array = list()
    # for test in tests:
    #     starttime = time.perf_counter()
    #     dijkstra(create_edges(test), 1, test - 1)
    #     print("Size "+ str(test) + " - "+str(int((time.perf_counter() - starttime)*1000000)) + " milliseconds")
    #     time_array.append((test,int((time.perf_counter() - starttime)*1000000)))
    #     starttime = 0
    #
    # for i in range(len(time_array)):
    #     test_array.append(time_array[i][0])
    #     times_array.append(time_array[i][1])
    #
    # df = pd.DataFrame({'Graph Size':test_array,'Time (milliSeconds)':times_array})
    #
    # sns.lineplot(data=df, x='Graph Size',y='Time (milliSeconds)')
    # plt.show()