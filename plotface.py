import urllib.request
import numpy as np
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs,  iplot

req = urllib.request.Request('file:../../GWAS/data/newref_face02_Samp.obj')
try:
    response=urllib.request.urlopen(req)
    obj_data = response.read().decode('utf-8') 
except urllib.error.URLError as e:
    print(e.reason)

def obj_to_mesh(odata):
    # odata is the string read from an obj file
    vertices = []
    faces = []
    lines = odata.splitlines()   
   
    for line in lines:
        slist = line.split()
        if slist:
            if slist[0] == 'v':
                vertex = list(map(float, slist[1:]))
                vertices.append(vertex)
            elif slist[0] == 'f':
                face = []
                for k in range(1, len(slist)):
                    face.append([int(s) for s in slist[k].replace('//','/').split('/')])
                
                if len(face) > 3: # triangulate the n-polyonal face, n>3
                    faces.extend([[face[0][0]-1, face[k][0]-1, face[k+1][0]-1] for k in range(1, len(face)-1)])
                else:    
                    faces.append([face[j][0]-1 for j in range(len(face))])
            else: pass
    
    
    return np.array(vertices), np.array(faces) 

pl_br = [[0.0, 'blue'],
         [0.2,  'cyan'],
         [0.4,  'green'],
         [0.6,  'yellow'],
         [0.8,  'orange'],
         [1.0,  'red'],
        ]
def plot3d(vtx,vc,trim,pl = pl_br,light = False):
    x,y,z = vtx.T
    I,J,K = trim.T

    mesh=dict(type='mesh3d',
              x=x,
              y=y,
              z=z,
              intensity=vc,  
              colorscale=pl,
              #vertexcolor=xm.T,#IMPORTANT! the color codes must be triplets of floats  in [0,1]!!
                                          #Plotly docs do not mention this requirement 
                                          #https://github.com/plotly/plotly.js/blob/master/src/traces/mesh3d/attributes.js#L150
              i=I,
              j=J,
              k=K,
              name='',
              showscale=False
            )
    if light:
        mesh.update(lighting=dict(ambient= 0.18,
                                  diffuse= 1,
                                  fresnel=  .1,
                                  specular= 1,
                                  roughness= .1),

                    lightposition=dict(x=100,
                                       y=200,
                                       z=150))

    layout = dict(title='',
                  font=dict(size=14, color='black'),
                  width=500,
                  height=500,
                  scene=dict(xaxis=dict(visible=False),
                             yaxis=dict(visible=False),  
                             zaxis=dict(visible=False), 
                             aspectratio=dict(x=0.78,
                                              y=1,
                                              z=0.58
                                             ),
                             camera=dict(up=dict(x=0, y=1, z=0),
                                         center=dict(x=0, y=0, z=0),
                                         eye=dict(x=0., y=0., z=1.5)),
                            ), 
                  #paper_bgcolor='rgb(235,235,235)',
                  #margin=dict(t=175)
                  margin = go.layout.Margin(
                      l=50,
                      r=50,
                      b=50,
                      t=50,
                      pad=4
                  ),
                  paper_bgcolor = 'LightSteelBlue',
            )

    fig = go.Figure(data=[mesh], layout=layout)
    iplot(fig)