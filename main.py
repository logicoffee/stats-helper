import math

import gradio as gr
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import beta
from statsmodels.stats.proportion import proportions_chisquare


def my_calc_sample_size(p1, p2, r):
    z_a = 1.64
    z_b = -0.84
    c1 = p1 * (1 - p1) * (1 / (1 - r) + 1 / r)
    c2 = p1 * (1 - p1) / (1 - r) + p2 * (1 - p2) / r
    n = ((z_a * math.sqrt(c1) - z_b * math.sqrt(c2)) / (p1 - p2)) ** 2
    n_a = n * (1 - r)
    n_b = n * r
    return n, n_a, n_b


def test(n_a, c_a, n_b, c_b):
    _, p_value, _ = proportions_chisquare(count=[c_a, c_b], nobs=[n_a, n_b])
    print(p_value)
    return p_value


def interval(n_a, c_a, n_b, c_b):
    p1 = c_a / n_a
    p2 = c_b / n_b
    sig = math.sqrt(p1 * (1 - p1) / n_a + p2 * (1 - p2) / n_b)
    z_a = 1.96
    lower = p1 - p2 - z_a * sig
    upper = p1 - p2 + z_a * sig
    return lower, upper


def plot(n_a, c_a, n_b, c_b):
    plt.close()
    x = np.linspace(0, 1, 101)
    y1 = beta.pdf(x, 1 + c_a, 1 + n_a - c_a)
    y2 = beta.pdf(x, 1 + c_b, 1 + n_b - c_b)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.savefig("foo.png")
    return "foo.png"


with gr.Blocks() as bl:
    gr.Markdown("# 2 群の母比率の検定")

    gr.Markdown("## サンプルサイズ")
    p_a = gr.Number(label="A 群の比率", value=0.1)
    p_b = gr.Number(label="B 群の比率", value=0.15)
    ratio = gr.Number(label="A 群と B 群のサンプルサイズの比率 (A 群 * ratio = B 群)", value=0.05)
    with gr.Row():
        sample_size = gr.Number(label="全体のサンプルサイズ")
        sample_size_a = gr.Number(label="A 群のサンプルサイズ")
        sample_size_b = gr.Number(label="B 群のサンプルサイズ")
    btn_ss = gr.Button("計算")
    btn_ss.click(
        my_calc_sample_size,
        inputs=[p_a, p_b, ratio],
        outputs=[sample_size, sample_size_a, sample_size_b],
    )

    gr.Markdown("## 検定")
    with gr.Row():
        n_a = gr.Number(label="A 群のサンプル数", value=100)
        c_a = gr.Number(label="A 群のコンバージョン数", value=20)
        r_a = gr.Number(label="A 群のコンバージョン率", value=0.2)
        c_a.input(lambda n, c: c / n, inputs=[n_a, c_a], outputs=r_a)
    with gr.Row():
        n_b = gr.Number(label="B 群のサンプル数", value=120)
        c_b = gr.Number(label="B 群のコンバージョン数", value=36)
        r_b = gr.Number(label="B 群のコンバージョン率", value=0.3)
        c_b.input(lambda n, c: c / n, inputs=[n_b, c_b], outputs=r_b)
    p_value = gr.Number(label="p 値")
    with gr.Row():
        lower = gr.Number(label="95% 信頼区間の下限")
        upper = gr.Number(label="95% 信頼区間の上限")
    image = gr.Image(height=400, width=600)
    btn_test = gr.Button("検定")
    btn_test.click(test, inputs=[n_a, c_a, n_b, c_b], outputs=p_value)
    btn_test.click(interval, inputs=[n_a, c_a, n_b, c_b], outputs=[lower, upper])
    btn_test.click(plot, inputs=[n_a, c_a, n_b, c_b], outputs=image)


bl.launch(server_name="0.0.0.0", server_port=7860)
