import stormpy


class TestBitvector:
    def test_init_default(self):
        bit = stormpy.BitVector()
        assert bit.size() == 0
        assert bit.number_of_set_bits() == 0

    def test_init_length(self):
        bit = stormpy.BitVector(10)
        assert bit.size() == 10
        assert bit.number_of_set_bits() == 0
        bit = stormpy.BitVector(5, True)
        assert bit.size() == 5
        assert bit.number_of_set_bits() == 5

    def test_init_vector(self):
        bit = stormpy.BitVector(5, [2, 3])
        assert bit.size() == 5
        assert bit.number_of_set_bits() == 2
        assert bit.get(0) is False
        assert bit.get(1) is False
        assert bit.get(2) is True
        assert bit.get(3) is True
        assert bit.get(4) is False

    def test_init_bitvector(self):
        bit = stormpy.BitVector(7, [0, 6])
        bit2 = stormpy.BitVector(bit)
        assert bit == bit2
        assert bit2.get(0) is True
        assert bit2.get(6) is True

    def test_negate(self):
        bit = stormpy.BitVector(7, [0, 6])
        bit2 = stormpy.BitVector(bit)
        bit = ~bit
        assert bit.get(0) is False
        assert bit.get(6) is False
        for i in range(bit.size()):
            assert bit.get(i) is not bit2.get(i)

    def test_resize_grow(self):
        bit = stormpy.BitVector(3, [0, 2])
        bit.resize(5)
        assert bit.size() == 5
        assert bit.get(0) is True
        assert bit.get(2) is True
        assert bit.get(3) is False
        assert bit.get(4) is False

    def test_resize_grow_init(self):
        bit = stormpy.BitVector(3, [0, 2])
        bit.resize(5, True)
        assert bit.size() == 5
        assert bit.get(3) is True
        assert bit.get(4) is True

    def test_resize_shrink(self):
        bit = stormpy.BitVector(5, [0, 4])
        bit.resize(3)
        assert bit.size() == 3
        assert bit.get(0) is True
        assert bit.get(1) is False
        assert bit.get(2) is False

    def test_complement(self):
        bit = stormpy.BitVector(7, [0, 6])
        bit2 = stormpy.BitVector(bit)
        bit.complement()
        assert bit.get(0) is False
        assert bit.get(6) is False
        for i in range(bit.size()):
            assert bit.get(i) is not bit2.get(i)

    def test_increment(self):
        bit = stormpy.BitVector(3, [0])
        bit.increment()
        assert bit.get(0) is False
        assert bit.get(1) is True
        assert bit.get(2) is False

    def test_increment_wraps_around(self):
        bit = stormpy.BitVector(3, True)
        bit.increment()
        assert bit.number_of_set_bits() == 0

    def test_is_subset_of(self):
        bit = stormpy.BitVector(5, [0, 2])
        other = stormpy.BitVector(5, [0, 1, 2])
        assert bit.is_subset_of(other) is True
        assert other.is_subset_of(bit) is False

    def test_is_disjoint_from(self):
        bit = stormpy.BitVector(5, [0, 1])
        other = stormpy.BitVector(5, [2, 3])
        assert bit.is_disjoint_from(other) is True
        overlapping = stormpy.BitVector(5, [1, 2])
        assert bit.is_disjoint_from(overlapping) is False

    def test_empty(self):
        bit = stormpy.BitVector(5)
        assert bit.empty() is True
        bit.set(2)
        assert bit.empty() is False

    def test_full(self):
        bit = stormpy.BitVector(5, True)
        assert bit.full() is True
        bit.set(2, False)
        assert bit.full() is False

    def test_clear(self):
        bit = stormpy.BitVector(5, True)
        bit.clear()
        assert bit.empty() is True
        assert bit.number_of_set_bits() == 0

    def test_fill(self):
        bit = stormpy.BitVector(5)
        bit.fill()
        assert bit.full() is True
        assert bit.number_of_set_bits() == 5

    def test_number_of_set_bits_before_index(self):
        bit = stormpy.BitVector(5, [1, 3])
        assert bit.number_of_set_bits_before_index(0) == 0
        assert bit.number_of_set_bits_before_index(2) == 1
        assert bit.number_of_set_bits_before_index(4) == 2

    def test_has_unique_set_bit(self):
        bit = stormpy.BitVector(5, [2])
        assert bit.has_unique_set_bit() is True
        empty_bit = stormpy.BitVector(5)
        assert empty_bit.has_unique_set_bit() is False
        multi_bit = stormpy.BitVector(5, [1, 2])
        assert multi_bit.has_unique_set_bit() is False

    def test_get_next_set_index(self):
        bit = stormpy.BitVector(5, [1, 3])
        assert bit.get_next_set_index(0) == 1
        assert bit.get_next_set_index(2) == 3
        assert bit.get_next_set_index(4) == 5

    def test_get_next_unset_index(self):
        bit = stormpy.BitVector(5, [0, 2])
        assert bit.get_next_unset_index(0) == 1
        assert bit.get_next_unset_index(2) == 3
        full_bit = stormpy.BitVector(5, True)
        assert full_bit.get_next_unset_index(0) == 5
