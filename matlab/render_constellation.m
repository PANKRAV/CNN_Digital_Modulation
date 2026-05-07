function img = render_constellation(rx_sig)

    img_size = 256;

    x = real(rx_sig);
    y = imag(rx_sig);

    x = (x + 2.5) / 5.0;
    y = (y + 2.5) / 5.0;

    px = round(x * (img_size - 1)) + 1;
    py = round(y * (img_size - 1)) + 1;

    valid = px >= 1 & px <= img_size & ...
            py >= 1 & py <= img_size;

    px = px(valid);
    py = py(valid);

    img = zeros(img_size, img_size, 'uint8');

    inds = sub2ind([img_size img_size], py, px);

    img(inds) = 255;

    img = flipud(img);

end