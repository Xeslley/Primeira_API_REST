from statsapi import operation
import pytest

def test_op_mean():
    # retira possiveis erros de aproximacoes
    assert operation.op_mean([1,2,3,4]) == pytest.approx(2.5)

def test_op_min(data):
    assert min(data)

def test_op_max(data):
    assert max(data)

def test_op_mean(data):
   assert np.mean(data)

def test_op_median(data):
   assert np.median(data)

# def test_op_mode(data):
#     assert np.mod(data)

def test_op_range(data):
    assert op_max(data) - op_min(data)