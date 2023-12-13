import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askstring
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Articulation Points Finder")

        
        self.style = ttk.Style()
        self.style.theme_use("clam")  

        self.graph = nx.Graph()
        self.points_of_articulation = set()

        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=root.destroy)

        toolbar = ttk.Frame(root, padding=(5, 2))
        toolbar.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(toolbar, text="Ajouter un sommet", command=self.add_vertex).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Ajouter une arrete", command=self.add_edge).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Trouver les points d'articulation", command=self.find_articulation).pack(side=tk.LEFT, padx=5)

        self.status_var = tk.StringVar()
        status_bar = ttk.Label(root, textvariable=self.status_var, anchor=tk.W, padding=(10, 2))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        main_frame = ttk.Frame(root)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas_frame = ttk.Frame(main_frame)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = FigureCanvasTkAgg(plt.Figure(figsize=(8, 6)))
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.draw_graph()

    def add_vertex(self):
        label = askstring("Ajouter un sommet", "Entrer un label pour le sommet:")
        if label:
            self.graph.add_node(label)
            self.draw_graph()

    def add_edge(self):
        vertices = askstring("Ajouter arrete", "Entrer les 2 sommets separé par un espace:").split()
        if len(vertices) == 2:
            self.graph.add_edge(vertices[0], vertices[1])
            self.draw_graph()

    def find_articulation(self):
        self.points_of_articulation = set(nx.articulation_points(self.graph))
        self.highlight_articulation_points()
        complexity = self.calculate_complexity()
        self.status_var.set(f"Complexity: {complexity}")

    def highlight_articulation_points(self):
        pos = nx.spring_layout(self.graph)
        colors = ['green' if node in self.points_of_articulation else 'blue' for node in self.graph.nodes]

        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        nx.draw_networkx_nodes(self.graph, pos, ax=ax, node_color=colors)
        nx.draw_networkx_edges(self.graph, pos, ax=ax)
        nx.draw_networkx_labels(self.graph, pos, ax=ax)
        self.canvas.draw()

    def calculate_complexity(self):
        num_vertices = len(self.graph.nodes)
        num_edges = len(self.graph.edges)
        complexity = num_vertices + num_edges
        return complexity

    def draw_graph(self):
        pos = nx.spring_layout(self.graph)
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        nx.draw_networkx_nodes(self.graph, pos, ax=ax)
        nx.draw_networkx_edges(self.graph, pos, ax=ax)
        nx.draw_networkx_labels(self.graph, pos, ax=ax)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
