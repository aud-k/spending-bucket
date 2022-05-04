import ipywidgets as widgets
from IPython.display import display, clear_output
import pickle
from SpendingBuckets import Bucket

class Application(widgets.AppLayout):
    
    def __init__(self):
        super().__init__()
        self.buckets = self.load_buckets()
        self.create_main_grid()
        self.create_new_button()
        self.create_exit_buttons()
        self.init_transfer()
        display(self)
    
    def create_main_grid(self):
        self.center = widgets.GridspecLayout(len(self.buckets)+1, 3)
        self.center[0, 0] = widgets.Label("Name:")
        self.center[0, 1] = widgets.Label("Balance:")
        for i, (name, bucket) in enumerate(self.buckets.items()):
            self.center[i, 0] = widgets.Label(name)
            self.center[i, 1] = widgets.Label(f"${bucket.balance}")
            btn = widgets.Button(description = f"New {name} Transaction")
            btn.on_click(self.create_new_transaction_widget(bucket))
            celf.center[i, 2] = btn
    
    def create_new_button(self):
        name_box = widgets.Text(
            placeholder="Name",
            description="New bucket name: "
        )
        new_button = widgets.Button(
            description = "New",
            tooltip = "Create new bucket"
        )
        new_button.on_click(self.new_bucket)
        self.header = widgets.HBox([name_box, new_button])
    
    def create_new_transaction_widget(self, bucket):
        self.transaction_widget = widgets.Box(
    
    def new_bucket(self, *args):
        name = self.header.children[0].value
        self.buckets[name] = Bucket(name)
        print(f"Created new bucket {name} with starting balance $0.00")
        self.create_main_grid() # Refresh the main grid with new values
        display(self)
    
    def create_exit_buttons(self):
        buttons = (widgets.Button(
            description = "Close",
            disabled=False,
            tooltip = "Close without saving"
        ), widgets.Button(
            description = "Save",
            tooltip = "Save bucket data"
        ))
        buttons[0].on_click(self.close_application)
        buttons[1].on_click(self.save_buckets)
        self.footer = widgets.HBox(buttons)
    
    def init_transfer(self, *args):
        from_box = widgets.Dropdown(options=[n for n in self.buckets.keys()], description="From Bucket:")
        to_box = widgets.Dropdown(options=[n for n in self.buckets.keys()], description="To Bucket:")
        amount_box = widgets.FloatText(description="Amount:")
        submit = widgets.Button(description="Submit")
        submit.on_click(self.transfer)
        self.right_sidebar = widgets.VBox([from_box, to_box, amount_box, submit])
    
    def transfer(self, *args):
        from_bucket = self.right_sidebar.children[0].value
        to_bucket = self.right_sidebar.children[1].value
        amount = self.right_sidebar.children[2].value
        self.buckets[from_bucket].move_to(amount, to_bucket)
        self.create_main_grid() # Refresh the main grid with new values
        display(self)
        
    def load_buckets(self):
        try:
            with open("bucketdata", 'rb') as f:
                buckets = pickle.load(f)
        except FileNotFoundError:
            print("bucketdata file not found!")
            return []
        return buckets
    
    def save_buckets(self, *args):
        with open("bucketdata", 'wb') as f:
            pickle.dump(self.buckets, f)
        print("Saved to bucketdata")
    
    def reset_buckets(self, *args):
        for b in self.buckets:
            b.reset()
    
    def close_application(self, *args):
        self.close()