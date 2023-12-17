import "@testing-library/jest-dom";
import { jestPreviewConfigure } from "jest-preview";
import "@/styles/globals.css";
import { server } from "./__test__/mocks/node";

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

jestPreviewConfigure({ autoPreview: true });
