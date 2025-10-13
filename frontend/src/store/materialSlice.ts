import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { MaterialInspection } from '../types';

interface MaterialState {
  items: MaterialInspection[];
  loading: boolean;
  error: string | null;
}

const initialState: MaterialState = {
  items: [],
  loading: false,
  error: null,
};

export const fetchMaterials = createAsyncThunk(
  'material/fetchMaterials',
  async () => {
    const response = await axios.get('/api/material/');
    return response.data;
  }
);

export const createMaterial = createAsyncThunk(
  'material/createMaterial',
  async (material: Partial<MaterialInspection>) => {
    const response = await axios.post('/api/material/', material);
    return response.data;
  }
);

const materialSlice = createSlice({
  name: 'material',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchMaterials.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchMaterials.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchMaterials.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch';
      })
      .addCase(createMaterial.fulfilled, (state, action) => {
        state.items.push(action.payload);
      });
  },
});

export default materialSlice.reducer;