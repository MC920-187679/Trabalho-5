"""
Operações de transformação linear puras.
"""
from typing import Optional
import numpy as np
from .tipos import OpLin


def identidade() -> OpLin:
    """
    Matriz identidade.
    """
    return np.eye(3, dtype=float)


def inversa(mat: OpLin) -> OpLin:
    """
    Matriz da transformação inversa.
    """
    return np.linalg.pinv(mat)


def escalonamento(Sx: float, Sy: Optional[float]=None) -> OpLin:
    """
    Matriz de mudança de escala.
    """
    if Sy is None:
        # escala repetida
        Sy = Sx

    return np.asarray([
        [Sx,  0,  0],
        [ 0, Sy,  0],
        [ 0,  0,  1]
    ], dtype=float)


def translacao(Tx: float, Ty: Optional[float]=None) -> OpLin:
    """
    Matriz de translação.
    """
    if Ty is None:
        # desvio repetido
        Ty = Tx

    return np.asarray([
        [ 1,  0, Tx],
        [ 0,  1, Ty],
        [ 0,  0,  1]
    ], dtype=float)


def rotacao(theta: float, *, graus: bool=True) -> OpLin:
    """
    Matriz de rotação no plano xy (em torno do eixo
    z) por um ângulo `theta`.
    """
    # transformação para radianos
    if graus:
        theta = np.deg2rad(theta)
    # seno e cosseno
    Ct, St = np.cos(theta), np.sin(theta)

    return np.asarray([
        [Ct,-St,  0],
        [St, Ct,  0],
        [ 0,  0,  1]
    ], dtype=float)


def rotacao_proj(beta: float, *, graus: bool=True, D: float=2.0) -> OpLin:
    """
    Matriz de rotação em torno do eixo y por um ângulo
    `beta`, projetado de volta para o plano xy.

    A imagem é considerada à uma distância `Z = D`
    e o foco está em `Z = -1`.
    """
    # transformação para radianos
    if graus:
        beta = np.deg2rad(beta)

    # criação do eixo Z
    G = np.asarray([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
        [0, 0, 1]
    ], dtype=float)

    # seno e cosseno
    Cb, Sb = np.cos(beta), np.sin(beta)
    # rotação em torno de y
    R = np.asarray([
        [ Cb, 0,Sb, 0],
        [  0, 1, 0, 0],
        [-Sb, 0,Cb, 0],
        [  0, 0, 0, 1]
    ], dtype=float)

    # translação para Z = D
    TD = np.asarray([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, D],
        [0, 0, 0, 1]
    ], dtype=float)

    # projeção com f = -1
    P = np.asarray([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 1]
    ], dtype=float)

    # correção de escala da projeção
    E = escalonamento(D + 1)

    return E @ P @ TD @ R @ G
