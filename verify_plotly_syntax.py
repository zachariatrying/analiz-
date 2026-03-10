import plotly.graph_objects as go

def verify_syntax():
    try:
        fig = go.Figure()
        print("Testing add_hline with 'line' argument...")
        # This matches the corrected code in app.py
        fig.add_hline(y=100, line=dict(color='rgba(255, 255, 255, 0.3)', width=1, dash='dash'))
        print("SUCCESS: add_hline executed without error.")
    except Exception as e:
        print(f"FAILURE: {e}")

if __name__ == "__main__":
    verify_syntax()

